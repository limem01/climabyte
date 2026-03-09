"""
ClimaByte - AI Engine
Uses Claude claude-sonnet-4-6 for receipt scanning (vision) and personalized coaching.
Falls back gracefully when API key is not available.
"""

import base64
import json
import re
from io import BytesIO

import streamlit as st

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

from carbon_data import FOOD_EMISSIONS, search_item


def get_anthropic_client():
    """Get Anthropic client with API key from secrets or env."""
    api_key = None
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        pass
    
    if not api_key:
        import os
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        api_key = "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"
    
    if api_key and HAS_ANTHROPIC:
        return anthropic.Anthropic(api_key=api_key)
    return None


def scan_receipt(image_bytes: bytes, mime_type: str = "image/jpeg") -> list:
    """
    Use Claude Vision to extract items from a receipt photo.
    Returns list of dicts: [{"item": "beef", "quantity": 1.5, "unit": "kg"}, ...]
    """
    client = get_anthropic_client()
    if not client:
        return None  # Signal that AI scanning is unavailable
    
    b64_image = base64.standard_b64encode(image_bytes).decode("utf-8")
    
    system_prompt = """You are a receipt/grocery item scanner for a carbon footprint app called ClimaByte. 
Your job is to extract food and grocery items from receipt photos or grocery list photos.

RULES:
1. Extract EVERY food/grocery item you can identify
2. Estimate quantity in kg (convert from lbs, units, etc.)
3. If quantity is unclear, estimate based on typical purchase amounts
4. Normalize item names to simple English (e.g., "organic free-range eggs 12pk" → "eggs")
5. Return ONLY valid JSON array, nothing else

Return format:
[
  {"item": "beef", "quantity": 1.0, "unit": "kg"},
  {"item": "milk", "quantity": 2.0, "unit": "kg"},
  {"item": "bananas", "quantity": 0.5, "unit": "kg"}
]

Common conversions:
- 1 dozen eggs ≈ 0.72 kg
- 1 gallon milk ≈ 3.9 kg
- 1 lb ≈ 0.45 kg
- 1 loaf bread ≈ 0.5 kg
- 1 can/tin ≈ 0.4 kg
- 1 bag chips ≈ 0.2 kg

If you cannot identify any food items, return: []"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": b64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Extract all food/grocery items from this receipt or grocery image. Return JSON array only."
                        }
                    ],
                }
            ],
        )
        
        raw = response.content[0].text.strip()
        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'\[.*\]', raw, re.DOTALL)
        if json_match:
            items = json.loads(json_match.group())
            return items
        return []
    
    except Exception as e:
        st.error(f"Receipt scanning error: {str(e)}")
        return None


def get_coach_message(cart_items: list, total_co2e: float, weekly_total: float = None) -> str:
    """
    Get a personalized coaching message from Claude based on the user's cart.
    """
    client = get_anthropic_client()
    if not client:
        return _fallback_coach_message(cart_items, total_co2e)
    
    cart_summary = "\n".join([
        f"- {item['name']}: {item['quantity']} {item['unit']} = {item['co2e_total']:.2f} kg CO2e"
        for item in cart_items
    ])
    
    system_prompt = """You are ClimaByte's Climate Coach — friendly, encouraging, data-driven, and never preachy.
You help people understand their carbon footprint through their shopping and daily choices.

PERSONALITY:
- Warm and supportive, like a knowledgeable friend
- Always lead with something positive before suggestions
- Use specific numbers and comparisons to make impact tangible
- Suggest realistic swaps, not extreme lifestyle changes
- Keep it brief (3-5 sentences max for quick coaching, up to 8 for detailed)
- Use analogies people relate to (driving distance, flights, trees)
- Never guilt-trip — empower with knowledge

FORMAT: Plain text, no markdown. Conversational tone."""

    user_msg = f"""Here's what the user just added to their carbon tracker:

{cart_summary}

Total carbon footprint: {total_co2e:.2f} kg CO2e
{"Weekly running total: " + f"{weekly_total:.2f} kg CO2e" if weekly_total else ""}

Give a brief, encouraging coaching message. Highlight the biggest impact item, suggest one realistic swap, and put the total in perspective (e.g., "That's like driving X km" or "equivalent to X hours of Netflix")."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": user_msg}],
        )
        return response.content[0].text.strip()
    except Exception:
        return _fallback_coach_message(cart_items, total_co2e)


def _fallback_coach_message(cart_items: list, total_co2e: float) -> str:
    """Generate a coaching message without AI — rule-based fallback."""
    if not cart_items:
        return "Add some items to see your carbon impact!"
    
    # Find highest impact item
    sorted_items = sorted(cart_items, key=lambda x: x["co2e_total"], reverse=True)
    top = sorted_items[0]
    
    driving_km = round(total_co2e / 0.192, 1)
    trees = round(total_co2e / 22, 2)
    
    msg = f"Your total footprint is {total_co2e:.2f} kg CO2e — equivalent to driving {driving_km} km in a gasoline car. "
    msg += f"The biggest contributor is {top['name']} at {top['co2e_total']:.2f} kg CO2e. "
    
    # Find the tip for the top item
    key = top.get("key", top["name"].lower().replace(" ", "_"))
    if key in FOOD_EMISSIONS:
        msg += FOOD_EMISSIONS[key]["tip"] + "."
    else:
        msg += "Small swaps add up — even replacing one high-impact item per week makes a real difference."
    
    if total_co2e > 10:
        msg += f" To offset this, you'd need about {trees} trees growing for a year."
    
    return msg


def get_weekly_insight(weekly_data: list) -> str:
    """Generate a weekly insight summary."""
    client = get_anthropic_client()
    
    total = sum(d.get("total_co2e", 0) for d in weekly_data)
    num_entries = len(weekly_data)
    
    if not client:
        avg_daily = total / max(num_entries, 1)
        yearly_proj = avg_daily * 365
        return (
            f"This week: {total:.1f} kg CO2e across {num_entries} sessions. "
            f"Daily average: {avg_daily:.1f} kg CO2e. "
            f"Projected annual food footprint: {yearly_proj:.0f} kg CO2e "
            f"(average Canadian: ~2,500 kg CO2e/year from food). "
            f"{'You are tracking below average — nice work!' if yearly_proj < 2500 else 'Look for high-impact swaps to bring this down.'}"
        )
    
    summary = json.dumps(weekly_data, indent=2)
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            temperature=0.7,
            system="You are ClimaByte's weekly report writer. Analyze the user's week of carbon tracking data and give a brief, encouraging summary with 1-2 specific improvement suggestions. Be data-driven and positive. 4-6 sentences max. Plain text, no markdown.",
            messages=[{
                "role": "user",
                "content": f"Here's my carbon tracking data for the week:\n{summary}\n\nTotal: {total:.2f} kg CO2e over {num_entries} tracking sessions."
            }],
        )
        return response.content[0].text.strip()
    except Exception:
        return _fallback_coach_message([], total)
