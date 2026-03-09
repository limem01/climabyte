"""
ClimaByte - Built-in Carbon Emission Factor Database
Sources: EPA, DEFRA, Climatiq OEFDB, peer-reviewed lifecycle analyses
All values in kg CO2e per unit (kg for food, kWh for energy, km for transport, etc.)
"""

# ── Food & Groceries (kg CO2e per kg of product) ──────────────────────────
FOOD_EMISSIONS = {
    # Meat & Animal Products
    "beef": {"co2e_per_kg": 27.0, "category": "Meat", "tip": "Try plant-based alternatives — even 1 meatless day/week saves ~100 kg CO2/year"},
    "lamb": {"co2e_per_kg": 24.0, "category": "Meat", "tip": "Lamb has a high footprint due to methane from digestion"},
    "pork": {"co2e_per_kg": 6.1, "category": "Meat", "tip": "Lower impact than beef, but plant proteins are still 5-10x lighter"},
    "chicken": {"co2e_per_kg": 4.3, "category": "Meat", "tip": "The lightest common meat — good swap from beef"},
    "turkey": {"co2e_per_kg": 4.5, "category": "Meat", "tip": "Similar footprint to chicken"},
    "fish": {"co2e_per_kg": 3.5, "category": "Seafood", "tip": "Wild-caught varies widely — farmed can be lower"},
    "salmon": {"co2e_per_kg": 5.4, "category": "Seafood", "tip": "Farmed salmon has moderate impact from feed production"},
    "tuna": {"co2e_per_kg": 3.1, "category": "Seafood", "tip": "Canned tuna is lower than fresh due to efficient processing"},
    "shrimp": {"co2e_per_kg": 11.8, "category": "Seafood", "tip": "Surprisingly high — mangrove destruction for shrimp farms adds emissions"},
    "prawns": {"co2e_per_kg": 11.8, "category": "Seafood", "tip": "Same as shrimp — high footprint from aquaculture"},
    "eggs": {"co2e_per_kg": 4.2, "category": "Dairy & Eggs", "tip": "Free-range may be slightly higher due to lower feed efficiency"},
    "milk": {"co2e_per_kg": 1.4, "category": "Dairy & Eggs", "tip": "Oat milk produces ~0.3 kg CO2e/L — 80% less"},
    "cheese": {"co2e_per_kg": 8.5, "category": "Dairy & Eggs", "tip": "Takes ~10L of milk per kg — concentrated emissions"},
    "butter": {"co2e_per_kg": 9.0, "category": "Dairy & Eggs", "tip": "Very concentrated dairy — use olive oil where possible"},
    "yogurt": {"co2e_per_kg": 1.7, "category": "Dairy & Eggs", "tip": "Plant-based yogurt cuts this by ~60%"},
    "cream": {"co2e_per_kg": 5.6, "category": "Dairy & Eggs", "tip": "High fat content = more milk = more emissions"},
    
    # Grains & Staples
    "rice": {"co2e_per_kg": 2.7, "category": "Grains", "tip": "Flooded rice paddies produce methane — try pasta or potatoes instead"},
    "pasta": {"co2e_per_kg": 1.2, "category": "Grains", "tip": "Low footprint staple — great base for meals"},
    "bread": {"co2e_per_kg": 1.0, "category": "Grains", "tip": "One of the lowest-footprint staples"},
    "flour": {"co2e_per_kg": 0.8, "category": "Grains", "tip": "Very low impact — baking at home is eco-friendly"},
    "oats": {"co2e_per_kg": 0.9, "category": "Grains", "tip": "Excellent low-carbon breakfast option"},
    "cereal": {"co2e_per_kg": 1.2, "category": "Grains", "tip": "Processing adds some emissions over raw grains"},
    "quinoa": {"co2e_per_kg": 1.3, "category": "Grains", "tip": "Despite transport from South America, still very low impact"},
    
    # Fruits & Vegetables
    "potatoes": {"co2e_per_kg": 0.3, "category": "Vegetables", "tip": "One of the lowest-carbon foods — versatile and filling"},
    "tomatoes": {"co2e_per_kg": 0.7, "category": "Vegetables", "tip": "Greenhouse-grown in winter can be 5x higher — buy seasonal"},
    "onions": {"co2e_per_kg": 0.3, "category": "Vegetables", "tip": "Very low impact and long shelf life"},
    "carrots": {"co2e_per_kg": 0.3, "category": "Vegetables", "tip": "Root vegetables are consistently low-carbon"},
    "broccoli": {"co2e_per_kg": 0.5, "category": "Vegetables", "tip": "Great nutrition-to-carbon ratio"},
    "spinach": {"co2e_per_kg": 0.4, "category": "Vegetables", "tip": "Leafy greens are almost always low-impact"},
    "lettuce": {"co2e_per_kg": 0.4, "category": "Vegetables", "tip": "Low carbon but also low calories — nutrient density matters"},
    "peppers": {"co2e_per_kg": 0.5, "category": "Vegetables", "tip": "Seasonal and local peppers have the lowest footprint"},
    "mushrooms": {"co2e_per_kg": 0.3, "category": "Vegetables", "tip": "Excellent meat substitute with tiny footprint"},
    "corn": {"co2e_per_kg": 0.5, "category": "Vegetables", "tip": "Efficient crop with low water and carbon needs"},
    "peas": {"co2e_per_kg": 0.4, "category": "Vegetables", "tip": "Nitrogen-fixing — actually improves soil health"},
    "beans": {"co2e_per_kg": 0.5, "category": "Legumes", "tip": "Best protein-to-carbon ratio of almost any food"},
    "lentils": {"co2e_per_kg": 0.4, "category": "Legumes", "tip": "Protein powerhouse with minimal footprint"},
    "chickpeas": {"co2e_per_kg": 0.5, "category": "Legumes", "tip": "Hummus is a climate-friendly snack"},
    "tofu": {"co2e_per_kg": 1.0, "category": "Legumes", "tip": "Even with processing, 27x lighter than beef per kg protein"},
    "soybeans": {"co2e_per_kg": 0.5, "category": "Legumes", "tip": "Deforestation-free soy is very low impact"},
    "apples": {"co2e_per_kg": 0.4, "category": "Fruits", "tip": "Local and seasonal apples are among the greenest fruits"},
    "bananas": {"co2e_per_kg": 0.7, "category": "Fruits", "tip": "Despite shipping, bananas are efficient — transported by boat"},
    "oranges": {"co2e_per_kg": 0.5, "category": "Fruits", "tip": "Citrus fruits have a relatively low footprint"},
    "berries": {"co2e_per_kg": 0.7, "category": "Fruits", "tip": "Frozen berries often have lower footprint than fresh air-shipped ones"},
    "avocado": {"co2e_per_kg": 1.3, "category": "Fruits", "tip": "Moderate footprint — water use is the bigger concern"},
    "grapes": {"co2e_per_kg": 0.5, "category": "Fruits", "tip": "Local grapes in season are very low impact"},
    "mango": {"co2e_per_kg": 0.9, "category": "Fruits", "tip": "Air-freighted mangoes can be much higher — check origin"},
    "pineapple": {"co2e_per_kg": 0.6, "category": "Fruits", "tip": "Boat-shipped pineapple is quite efficient"},
    
    # Nuts & Seeds
    "almonds": {"co2e_per_kg": 2.3, "category": "Nuts", "tip": "Water-intensive but still much lower than dairy"},
    "peanuts": {"co2e_per_kg": 1.2, "category": "Nuts", "tip": "Nitrogen-fixing crop — relatively efficient"},
    "cashews": {"co2e_per_kg": 2.1, "category": "Nuts", "tip": "Processing is energy-intensive but still low overall"},
    "walnuts": {"co2e_per_kg": 1.8, "category": "Nuts", "tip": "Tree crops sequester carbon while growing"},
    
    # Beverages
    "coffee": {"co2e_per_kg": 5.0, "category": "Beverages", "tip": "~0.05 kg CO2e per cup — moderate. Shade-grown is better"},
    "tea": {"co2e_per_kg": 1.9, "category": "Beverages", "tip": "Very low per cup (~0.02 kg CO2e) — one of the lightest drinks"},
    "beer": {"co2e_per_kg": 0.8, "category": "Beverages", "tip": "~0.3 kg CO2e per pint — moderate"},
    "wine": {"co2e_per_kg": 1.4, "category": "Beverages", "tip": "~0.2 kg CO2e per glass — glass bottle is most of the footprint"},
    "juice": {"co2e_per_kg": 0.8, "category": "Beverages", "tip": "Whole fruit is more efficient — less processing waste"},
    "soda": {"co2e_per_kg": 0.4, "category": "Beverages", "tip": "Low carbon but zero nutrition — water is better all around"},
    
    # Oils & Condiments
    "olive oil": {"co2e_per_kg": 3.5, "category": "Oils", "tip": "Higher than seed oils but healthier — use mindfully"},
    "vegetable oil": {"co2e_per_kg": 2.5, "category": "Oils", "tip": "Canola/sunflower are among the lowest-impact oils"},
    "coconut oil": {"co2e_per_kg": 2.1, "category": "Oils", "tip": "Relatively low if sourced sustainably"},
    "sugar": {"co2e_per_kg": 1.2, "category": "Pantry", "tip": "Beet sugar (temperate) is lower than cane sugar (tropical)"},
    "chocolate": {"co2e_per_kg": 4.5, "category": "Pantry", "tip": "Cocoa farming drives deforestation — look for Rainforest Alliance certified"},
    
    # Processed & Ready Meals
    "pizza": {"co2e_per_kg": 3.0, "category": "Processed", "tip": "Cheese is the main driver — veggie pizza cuts ~40%"},
    "burger": {"co2e_per_kg": 8.0, "category": "Processed", "tip": "A single beef burger ≈ 3.5 kg CO2e — plant-based is ~0.5 kg"},
    "sausage": {"co2e_per_kg": 5.5, "category": "Processed", "tip": "Pork sausage is lower than beef — plant-based lowest"},
    "bacon": {"co2e_per_kg": 6.5, "category": "Processed", "tip": "High processing + pork = moderate-high footprint"},
    "ice cream": {"co2e_per_kg": 3.8, "category": "Processed", "tip": "Dairy-based — oat/coconut ice cream cuts emissions ~60%"},
    "chips": {"co2e_per_kg": 1.8, "category": "Processed", "tip": "Frying and packaging add to the potato's low base"},
    "frozen meals": {"co2e_per_kg": 3.5, "category": "Processed", "tip": "Varies wildly — check if meat-based or plant-based"},
}

# ── Transport (kg CO2e per km per person) ─────────────────────────────────
TRANSPORT_EMISSIONS = {
    "car_gasoline": {"co2e_per_km": 0.192, "label": "Car (Gasoline)", "tip": "Carpooling with 1 extra person cuts your per-person emissions in half"},
    "car_diesel": {"co2e_per_km": 0.171, "label": "Car (Diesel)", "tip": "Slightly more efficient than gasoline but produces more NOx"},
    "car_hybrid": {"co2e_per_km": 0.108, "label": "Car (Hybrid)", "tip": "~40% less than pure gasoline — great transition option"},
    "car_electric": {"co2e_per_km": 0.047, "label": "Car (Electric)", "tip": "75% less than gasoline — even better with renewable grid power"},
    "bus": {"co2e_per_km": 0.089, "label": "Bus", "tip": "Per passenger, buses are very efficient — especially when full"},
    "train": {"co2e_per_km": 0.041, "label": "Train", "tip": "One of the lowest-carbon ways to travel — 80% less than driving alone"},
    "subway": {"co2e_per_km": 0.031, "label": "Subway/Metro", "tip": "Electric rail is extremely efficient per passenger"},
    "bicycle": {"co2e_per_km": 0.0, "label": "Bicycle", "tip": "Zero direct emissions — the gold standard of green transport"},
    "walking": {"co2e_per_km": 0.0, "label": "Walking", "tip": "Zero emissions and good for health — win-win"},
    "motorcycle": {"co2e_per_km": 0.103, "label": "Motorcycle", "tip": "More efficient than a car for single passengers"},
    "flight_short": {"co2e_per_km": 0.255, "label": "Flight (<1500km)", "tip": "Short flights are worst per km — consider train if under 600km"},
    "flight_long": {"co2e_per_km": 0.195, "label": "Flight (>1500km)", "tip": "Longer flights are more efficient per km but total impact is huge"},
    "ferry": {"co2e_per_km": 0.019, "label": "Ferry", "tip": "Quite efficient — especially modern electric ferries"},
    "taxi": {"co2e_per_km": 0.210, "label": "Taxi/Rideshare", "tip": "Similar to driving alone — shared rides cut it significantly"},
    "scooter_electric": {"co2e_per_km": 0.015, "label": "E-Scooter", "tip": "Very low emissions — great for short urban trips"},
}

# ── Home Energy (kg CO2e per kWh or per unit) ────────────────────────────
ENERGY_EMISSIONS = {
    "electricity_us": {"co2e_per_kwh": 0.417, "label": "Electricity (US avg)", "tip": "Switch to green energy provider or add solar panels"},
    "electricity_eu": {"co2e_per_kwh": 0.276, "label": "Electricity (EU avg)", "tip": "EU grid is cleaner than US due to more renewables"},
    "electricity_canada": {"co2e_per_kwh": 0.120, "label": "Electricity (Canada avg)", "tip": "Canada's grid is relatively clean — heavy hydro"},
    "electricity_quebec": {"co2e_per_kwh": 0.002, "label": "Electricity (Quebec)", "tip": "Quebec is 99% hydro — your electricity is nearly zero-carbon!"},
    "natural_gas": {"co2e_per_kwh": 0.205, "label": "Natural Gas", "tip": "Heat pumps can replace gas heating at 3-4x efficiency"},
    "heating_oil": {"co2e_per_kwh": 0.265, "label": "Heating Oil", "tip": "One of the dirtiest heating options — consider switching"},
    "propane": {"co2e_per_kwh": 0.215, "label": "Propane", "tip": "Slightly cleaner than oil but still fossil fuel"},
    "solar": {"co2e_per_kwh": 0.0, "label": "Solar", "tip": "Zero operational emissions — pays back in ~2-3 years"},
    "wind": {"co2e_per_kwh": 0.0, "label": "Wind", "tip": "Zero operational emissions"},
}

# ── Everyday Items (kg CO2e per item or per use) ─────────────────────────
LIFESTYLE_EMISSIONS = {
    "plastic_bag": {"co2e": 0.033, "unit": "bag", "tip": "Bring reusable bags — 1 reusable = 500+ plastic bags saved"},
    "plastic_bottle": {"co2e": 0.082, "unit": "bottle", "tip": "A reusable bottle saves ~150 plastic bottles/year"},
    "paper_bag": {"co2e": 0.080, "unit": "bag", "tip": "Surprisingly higher than plastic per use — reusable is best"},
    "cotton_tshirt": {"co2e": 8.0, "unit": "shirt", "tip": "Buy second-hand or quality that lasts — fast fashion is wasteful"},
    "jeans": {"co2e": 33.0, "unit": "pair", "tip": "One pair of jeans = 33 kg CO2e — buy durable, repair when possible"},
    "smartphone": {"co2e": 70.0, "unit": "device", "tip": "Keep your phone 3-4 years instead of 2 — cuts lifecycle impact 40%"},
    "laptop": {"co2e": 300.0, "unit": "device", "tip": "Manufacturing is 80% of a laptop's lifetime emissions"},
    "load_laundry": {"co2e": 0.6, "unit": "load", "tip": "Wash cold and air-dry — cuts laundry emissions by 75%"},
    "shower_8min": {"co2e": 0.8, "unit": "shower", "tip": "Cutting to 5 min saves ~40% — low-flow head helps more"},
    "streaming_1hr": {"co2e": 0.036, "unit": "hour", "tip": "Lower resolution = less data = less server energy"},
    "google_search": {"co2e": 0.0003, "unit": "search", "tip": "Tiny per search but adds up — 8.5 billion searches/day globally"},
    "email": {"co2e": 0.004, "unit": "email", "tip": "Attachments increase this 50x — use links instead"},
    "email_spam": {"co2e": 0.003, "unit": "email", "tip": "Unsubscribe from spam — saves energy and your time"},
}

# ── Averages for comparison ──────────────────────────────────────────────
ANNUAL_AVERAGES = {
    "world": 4.7,        # tonnes CO2e per person per year
    "us": 15.5,
    "canada": 14.2,
    "eu": 6.8,
    "uk": 5.5,
    "china": 7.4,
    "india": 1.9,
    "france": 4.6,
    "germany": 8.9,
    "japan": 9.0,
    "brazil": 2.3,
    "australia": 15.4,
    "paris_target": 2.3,  # The 2030 target for 1.5°C pathway
}

# ── Equivalencies (for making numbers tangible) ──────────────────────────
def get_equivalencies(co2e_kg: float) -> dict:
    """Convert kg CO2e into relatable equivalencies."""
    return {
        "driving_km": round(co2e_kg / 0.192, 1),             # km in gasoline car
        "flights_nyc_london": round(co2e_kg / 986, 2),       # round trips NYC-London
        "trees_to_offset": round(co2e_kg / 22, 1),           # trees needed for 1 year
        "smartphone_charges": round(co2e_kg / 0.008, 0),     # full smartphone charges
        "beef_burgers": round(co2e_kg / 3.5, 1),             # beef burgers equivalent
        "hours_streaming": round(co2e_kg / 0.036, 0),        # hours of Netflix
        "led_bulb_hours": round(co2e_kg / 0.005, 0),         # hours of LED light
        "showers": round(co2e_kg / 0.8, 1),                  # 8-min showers
    }


def search_item(query: str) -> list:
    """Search across all databases for matching items."""
    query_lower = query.lower().strip()
    results = []
    
    for name, data in FOOD_EMISSIONS.items():
        if query_lower in name.lower() or name.lower() in query_lower:
            results.append({
                "name": name.replace("_", " ").title(),
                "key": name,
                "type": "food",
                "co2e": data["co2e_per_kg"],
                "unit": "kg",
                "category": data["category"],
                "tip": data["tip"],
            })
    
    for name, data in TRANSPORT_EMISSIONS.items():
        if query_lower in data["label"].lower() or query_lower in name.replace("_", " "):
            results.append({
                "name": data["label"],
                "key": name,
                "type": "transport",
                "co2e": data["co2e_per_km"],
                "unit": "km",
                "category": "Transport",
                "tip": data["tip"],
            })
    
    for name, data in ENERGY_EMISSIONS.items():
        if query_lower in data["label"].lower() or query_lower in name.replace("_", " "):
            results.append({
                "name": data["label"],
                "key": name,
                "type": "energy",
                "co2e": data["co2e_per_kwh"],
                "unit": "kWh",
                "category": "Energy",
                "tip": data["tip"],
            })
    
    for name, data in LIFESTYLE_EMISSIONS.items():
        if query_lower in name.replace("_", " "):
            results.append({
                "name": name.replace("_", " ").title(),
                "key": name,
                "type": "lifestyle",
                "co2e": data["co2e"],
                "unit": data["unit"],
                "category": "Lifestyle",
                "tip": data["tip"],
            })
    
    return results


def get_all_food_items() -> list:
    """Get all food items sorted by category."""
    items = []
    for name, data in FOOD_EMISSIONS.items():
        items.append({
            "name": name.replace("_", " ").title(),
            "key": name,
            "co2e_per_kg": data["co2e_per_kg"],
            "category": data["category"],
        })
    return sorted(items, key=lambda x: (x["category"], x["name"]))
