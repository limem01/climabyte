"""
ClimaByte — AI-Powered Personal Carbon Footprint Tracker
Frostbyte Hackathon 2026 | Sustainability & Climate Tech

Scan receipts with Claude Vision, track your carbon footprint,
get personalized AI coaching to reduce your impact.
"""

import datetime
import json

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

from carbon_data import (
    ANNUAL_AVERAGES,
    ENERGY_EMISSIONS,
    FOOD_EMISSIONS,
    LIFESTYLE_EMISSIONS,
    TRANSPORT_EMISSIONS,
    get_all_food_items,
    get_equivalencies,
    search_item,
)
from ai_engine import get_coach_message, scan_receipt, get_weekly_insight

# ── Page Config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClimaByte",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #1a2940 50%, #0d2137 100%);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        background: linear-gradient(120deg, #00d4aa, #00b4d8, #48cae4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }
    .main-header p {
        color: #8ba3c4;
        font-size: 1.1rem;
        margin-top: 0.3rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4aa;
        margin: 0;
    }
    .metric-label {
        color: #8ba3c4;
        font-size: 0.85rem;
        margin: 0;
    }
    .metric-delta-good {
        color: #00d4aa;
        font-size: 0.9rem;
    }
    .metric-delta-bad {
        color: #ff6b6b;
        font-size: 0.9rem;
    }
    
    /* Cart item styling */
    .cart-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Coach message */
    .coach-box {
        background: linear-gradient(135deg, rgba(0,212,170,0.08), rgba(0,180,216,0.08));
        border: 1px solid rgba(0,212,170,0.2);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        color: #c8dce8;
        line-height: 1.6;
    }
    .coach-box .coach-label {
        color: #00d4aa;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    /* Tip cards */
    .tip-card {
        background: rgba(0,212,170,0.06);
        border-left: 3px solid #00d4aa;
        border-radius: 0 12px 12px 0;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        color: #a8c4d4;
        font-size: 0.9rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(10, 22, 40, 0.95);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.04);
        border-radius: 8px;
        color: #8ba3c4;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0,212,170,0.15);
        color: #00d4aa;
        border-color: rgba(0,212,170,0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Session State Init ───────────────────────────────────────────────────
if "cart" not in st.session_state:
    st.session_state.cart = []
if "history" not in st.session_state:
    st.session_state.history = []  # List of daily totals
if "weekly_data" not in st.session_state:
    st.session_state.weekly_data = []
if "coach_message" not in st.session_state:
    st.session_state.coach_message = ""
if "total_tracked" not in st.session_state:
    st.session_state.total_tracked = 0.0

# ── Helper Functions ─────────────────────────────────────────────────────
def add_to_cart(name: str, key: str, quantity: float, unit: str, co2e_per_unit: float, category: str, tip: str = "", item_type: str = "food"):
    """Add an item to the cart."""
    co2e_total = quantity * co2e_per_unit
    st.session_state.cart.append({
        "name": name,
        "key": key,
        "quantity": quantity,
        "unit": unit,
        "co2e_per_unit": co2e_per_unit,
        "co2e_total": co2e_total,
        "category": category,
        "tip": tip,
        "type": item_type,
        "timestamp": datetime.datetime.now().isoformat(),
    })
    st.session_state.total_tracked += co2e_total

def get_cart_total() -> float:
    return sum(item["co2e_total"] for item in st.session_state.cart)

def clear_cart():
    if st.session_state.cart:
        total = get_cart_total()
        st.session_state.history.append({
            "date": datetime.datetime.now().isoformat(),
            "total_co2e": total,
            "items": len(st.session_state.cart),
        })
        st.session_state.weekly_data.append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_co2e": total,
            "items": [{"name": i["name"], "co2e": i["co2e_total"]} for i in st.session_state.cart],
        })
    st.session_state.cart = []
    st.session_state.coach_message = ""

# ── Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌍 ClimaByte</h1>
    <p>AI-Powered Personal Carbon Footprint Tracker</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Your Impact")
    
    total_session = get_cart_total()
    total_all_time = st.session_state.total_tracked
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Cart", f"{total_session:.2f} kg", label_visibility="visible")
    with col2:
        st.metric("All Sessions", f"{total_all_time:.1f} kg", label_visibility="visible")
    
    st.markdown("---")
    
    # Quick equivalencies for current cart
    if total_session > 0:
        eq = get_equivalencies(total_session)
        st.markdown("**That's equivalent to:**")
        st.markdown(f"🚗 Driving **{eq['driving_km']} km**")
        st.markdown(f"🌳 Needs **{eq['trees_to_offset']} trees** (1 year)")
        st.markdown(f"🍔 **{eq['beef_burgers']} beef burgers**")
        st.markdown(f"📱 **{int(eq['smartphone_charges'])}** phone charges")
    
    st.markdown("---")
    
    # Country comparison
    st.markdown("### 🌐 Annual Averages (tonnes CO2e)")
    country_data = {
        "Country": ["World", "US", "Canada", "EU", "UK", "China", "India", "Paris 1.5°C Target"],
        "Tonnes CO2e": [
            ANNUAL_AVERAGES["world"], ANNUAL_AVERAGES["us"], ANNUAL_AVERAGES["canada"],
            ANNUAL_AVERAGES["eu"], ANNUAL_AVERAGES["uk"], ANNUAL_AVERAGES["china"],
            ANNUAL_AVERAGES["india"], ANNUAL_AVERAGES["paris_target"],
        ]
    }
    fig_bar = px.bar(
        country_data, x="Tonnes CO2e", y="Country", orientation="h",
        color="Tonnes CO2e",
        color_continuous_scale=["#00d4aa", "#ffd166", "#ff6b6b"],
        height=300,
    )
    fig_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#8ba3c4",
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=10, t=10, b=10),
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#4a6580; font-size:0.8rem;'>"
        "Built with Claude AI + Climatiq Data<br>"
        "Frostbyte Hackathon 2026"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Main Tabs ────────────────────────────────────────────────────────────
tab_scan, tab_manual, tab_transport, tab_home, tab_dashboard, tab_learn = st.tabs([
    "📸 Scan Receipt", "🛒 Add Items", "🚗 Transport", "🏠 Home Energy", "📈 Dashboard", "📚 Learn"
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: SCAN RECEIPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_scan:
    st.markdown("### 📸 Scan a Receipt or Grocery Photo")
    st.markdown("Upload a photo of your grocery receipt or shopping haul — Claude Vision will extract the items and calculate your carbon footprint automatically.")
    
    uploaded = st.file_uploader(
        "Upload receipt image",
        type=["jpg", "jpeg", "png", "webp"],
        key="receipt_upload",
    )
    
    if uploaded:
        col_img, col_results = st.columns([1, 1.5])
        
        with col_img:
            image = Image.open(uploaded)
            st.image(image, caption="Your receipt", use_container_width=True)
        
        with col_results:
            with st.spinner("🔍 Claude is scanning your receipt..."):
                image_bytes = uploaded.getvalue()
                mime = uploaded.type or "image/jpeg"
                scanned_items = scan_receipt(image_bytes, mime)
            
            if scanned_items is None:
                st.warning("AI scanning requires an Anthropic API key. Add it to `.streamlit/secrets.toml` or use the Manual tab to add items.")
            elif len(scanned_items) == 0:
                st.info("No food items detected. Try a clearer photo or use the Manual tab.")
            else:
                st.success(f"Found **{len(scanned_items)} items** on your receipt!")
                
                for item in scanned_items:
                    item_name = item.get("item", "").lower().strip()
                    quantity = float(item.get("quantity", 1.0))
                    
                    # Match to our database
                    matches = search_item(item_name)
                    if matches:
                        match = matches[0]
                        co2e = match["co2e"] * quantity
                        st.markdown(
                            f"**{match['name']}** — {quantity} {match['unit']} — "
                            f"**{co2e:.2f} kg CO2e**"
                        )
                    else:
                        st.markdown(f"**{item_name.title()}** — {quantity} kg — *(no emission data)*")
                
                if st.button("➕ Add all scanned items to cart", type="primary", key="add_scanned"):
                    added = 0
                    for item in scanned_items:
                        item_name = item.get("item", "").lower().strip()
                        quantity = float(item.get("quantity", 1.0))
                        matches = search_item(item_name)
                        if matches:
                            m = matches[0]
                            add_to_cart(
                                name=m["name"], key=m["key"], quantity=quantity,
                                unit=m["unit"], co2e_per_unit=m["co2e"],
                                category=m["category"], tip=m.get("tip", ""),
                                item_type=m["type"],
                            )
                            added += 1
                    st.success(f"Added {added} items to your cart!")
                    st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: MANUAL ADD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_manual:
    st.markdown("### 🛒 Add Food & Grocery Items")
    
    col_search, col_browse = st.columns([1.5, 1])
    
    with col_search:
        st.markdown("**Search for an item:**")
        query = st.text_input("Type a food item...", placeholder="e.g., beef, rice, coffee, cheese", key="food_search")
        
        if query:
            results = search_item(query)
            if results:
                for r in results[:8]:
                    col_name, col_qty, col_btn = st.columns([2, 1, 1])
                    with col_name:
                        st.markdown(f"**{r['name']}** — {r['co2e']} kg CO2e/{r['unit']}")
                        st.caption(f"*{r['tip']}*")
                    with col_qty:
                        qty = st.number_input(
                            f"Qty ({r['unit']})", min_value=0.1, value=1.0, step=0.1,
                            key=f"qty_{r['key']}_{r['type']}",
                        )
                    with col_btn:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Add", key=f"add_{r['key']}_{r['type']}", type="primary"):
                            add_to_cart(
                                name=r["name"], key=r["key"], quantity=qty,
                                unit=r["unit"], co2e_per_unit=r["co2e"],
                                category=r["category"], tip=r.get("tip", ""),
                                item_type=r["type"],
                            )
                            st.rerun()
            else:
                st.info("No match found. Try a simpler term (e.g., 'beef' instead of 'ground beef').")
    
    with col_browse:
        st.markdown("**Quick Add (Common Items):**")
        quick_items = ["beef", "chicken", "rice", "milk", "cheese", "eggs", "bread", "pasta", "coffee", "bananas", "potatoes", "tofu"]
        
        for item_key in quick_items:
            data = FOOD_EMISSIONS.get(item_key)
            if data:
                if st.button(
                    f"{item_key.title()} ({data['co2e_per_kg']} kg CO2e/kg)",
                    key=f"quick_{item_key}",
                    use_container_width=True,
                ):
                    add_to_cart(
                        name=item_key.title(), key=item_key, quantity=1.0,
                        unit="kg", co2e_per_unit=data["co2e_per_kg"],
                        category=data["category"], tip=data["tip"],
                    )
                    st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: TRANSPORT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_transport:
    st.markdown("### 🚗 Track Transport Emissions")
    st.markdown("Log your daily commute or trips to see the carbon impact.")
    
    col_mode, col_dist = st.columns(2)
    
    with col_mode:
        transport_options = {k: v["label"] for k, v in TRANSPORT_EMISSIONS.items()}
        selected_transport = st.selectbox(
            "Mode of transport",
            options=list(transport_options.keys()),
            format_func=lambda x: transport_options[x],
            key="transport_mode",
        )
    
    with col_dist:
        distance = st.number_input("Distance (km)", min_value=0.1, value=10.0, step=1.0, key="transport_dist")
    
    t_data = TRANSPORT_EMISSIONS[selected_transport]
    co2e_transport = distance * t_data["co2e_per_km"]
    
    st.markdown(f"**Estimated emissions: {co2e_transport:.2f} kg CO2e**")
    
    # Comparison chart
    comparison_data = []
    for key, data in TRANSPORT_EMISSIONS.items():
        if key not in ["walking", "bicycle"]:  # Skip zero-emission for visual clarity
            comparison_data.append({
                "Mode": data["label"],
                "kg CO2e": round(distance * data["co2e_per_km"], 2),
                "Selected": "Selected" if key == selected_transport else "Other",
            })
    
    fig_transport = px.bar(
        comparison_data, x="Mode", y="kg CO2e", color="Selected",
        color_discrete_map={"Selected": "#00d4aa", "Other": "rgba(255,255,255,0.15)"},
        title=f"Comparison: {distance} km by different modes",
        height=350,
    )
    fig_transport.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#8ba3c4",
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig_transport, use_container_width=True)
    
    st.markdown(f'<div class="tip-card">💡 {t_data["tip"]}</div>', unsafe_allow_html=True)
    
    if st.button("➕ Add to cart", type="primary", key="add_transport"):
        add_to_cart(
            name=t_data["label"], key=selected_transport, quantity=distance,
            unit="km", co2e_per_unit=t_data["co2e_per_km"],
            category="Transport", tip=t_data["tip"], item_type="transport",
        )
        st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4: HOME ENERGY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_home:
    st.markdown("### 🏠 Home Energy Tracker")
    st.markdown("Track your electricity and heating to understand your home's carbon impact.")
    
    col_source, col_usage = st.columns(2)
    
    with col_source:
        energy_options = {k: v["label"] for k, v in ENERGY_EMISSIONS.items()}
        selected_energy = st.selectbox(
            "Energy source",
            options=list(energy_options.keys()),
            format_func=lambda x: energy_options[x],
            key="energy_source",
        )
    
    with col_usage:
        kwh = st.number_input("Usage (kWh)", min_value=1.0, value=100.0, step=10.0, key="energy_kwh")
    
    e_data = ENERGY_EMISSIONS[selected_energy]
    co2e_energy = kwh * e_data["co2e_per_kwh"]
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Carbon Footprint", f"{co2e_energy:.2f} kg CO2e")
    with col_m2:
        st.metric("Per kWh", f"{e_data['co2e_per_kwh']:.3f} kg CO2e")
    with col_m3:
        monthly_proj = co2e_energy * (720 / max(kwh, 1))  # Project to avg monthly use
        st.metric("Monthly Estimate", f"{co2e_energy * 3:.1f} kg CO2e")
    
    st.markdown(f'<div class="tip-card">💡 {e_data["tip"]}</div>', unsafe_allow_html=True)
    
    # Energy source comparison
    energy_compare = []
    for key, data in ENERGY_EMISSIONS.items():
        energy_compare.append({
            "Source": data["label"],
            "kg CO2e per kWh": data["co2e_per_kwh"],
        })
    
    fig_energy = px.bar(
        energy_compare, x="Source", y="kg CO2e per kWh",
        color="kg CO2e per kWh",
        color_continuous_scale=["#00d4aa", "#ffd166", "#ff6b6b"],
        title="Carbon Intensity by Energy Source",
        height=300,
    )
    fig_energy.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#8ba3c4",
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig_energy, use_container_width=True)
    
    if st.button("➕ Add to cart", type="primary", key="add_energy"):
        add_to_cart(
            name=e_data["label"], key=selected_energy, quantity=kwh,
            unit="kWh", co2e_per_unit=e_data["co2e_per_kwh"],
            category="Energy", tip=e_data["tip"], item_type="energy",
        )
        st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 5: DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_dashboard:
    st.markdown("### 📈 Your Carbon Dashboard")
    
    if not st.session_state.cart and not st.session_state.history:
        st.info("Start adding items to see your dashboard come to life! Use the tabs above to scan receipts, add food, log transport, or track energy.")
    else:
        # Top metrics
        total = get_cart_total()
        num_items = len(st.session_state.cart)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Session", f"{total:.2f} kg CO2e")
        with col2:
            st.metric("Items Tracked", str(num_items))
        with col3:
            avg_per_item = total / max(num_items, 1)
            st.metric("Avg per Item", f"{avg_per_item:.2f} kg")
        with col4:
            yearly_proj = total * 365 / max(1, 1)  # Very rough
            st.metric("Sessions Logged", str(len(st.session_state.history)))
        
        # Cart breakdown by category
        if st.session_state.cart:
            st.markdown("---")
            
            col_chart, col_coach = st.columns([1.2, 1])
            
            with col_chart:
                # Category breakdown pie chart
                category_totals = {}
                for item in st.session_state.cart:
                    cat = item["category"]
                    category_totals[cat] = category_totals.get(cat, 0) + item["co2e_total"]
                
                fig_pie = px.pie(
                    names=list(category_totals.keys()),
                    values=list(category_totals.values()),
                    title="Carbon Footprint by Category",
                    color_discrete_sequence=["#00d4aa", "#00b4d8", "#48cae4", "#ffd166", "#ff6b6b", "#c77dff", "#72efdd"],
                    hole=0.4,
                )
                fig_pie.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#8ba3c4",
                    margin=dict(l=10, r=10, t=40, b=10),
                    height=350,
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Item breakdown bar chart
                item_data = sorted(st.session_state.cart, key=lambda x: x["co2e_total"], reverse=True)
                fig_items = px.bar(
                    x=[i["name"] for i in item_data],
                    y=[i["co2e_total"] for i in item_data],
                    title="Carbon Footprint by Item",
                    labels={"x": "Item", "y": "kg CO2e"},
                    color=[i["co2e_total"] for i in item_data],
                    color_continuous_scale=["#00d4aa", "#ffd166", "#ff6b6b"],
                    height=350,
                )
                fig_items.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#8ba3c4",
                    showlegend=False,
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=40, b=10),
                    xaxis_tickangle=-45,
                )
                st.plotly_chart(fig_items, use_container_width=True)
            
            with col_coach:
                st.markdown("#### 🤖 AI Climate Coach")
                
                if st.button("Get AI Coaching", type="primary", key="get_coaching"):
                    with st.spinner("Thinking..."):
                        weekly_total = sum(d["total_co2e"] for d in st.session_state.weekly_data) + total
                        st.session_state.coach_message = get_coach_message(
                            st.session_state.cart, total, weekly_total
                        )
                
                if st.session_state.coach_message:
                    st.markdown(
                        f'<div class="coach-box">'
                        f'<div class="coach-label">🌱 Climate Coach</div>'
                        f'{st.session_state.coach_message}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                
                # Tips from items
                st.markdown("#### 💡 Tips for Your Items")
                shown_tips = set()
                for item in sorted(st.session_state.cart, key=lambda x: x["co2e_total"], reverse=True):
                    if item["tip"] and item["tip"] not in shown_tips:
                        st.markdown(
                            f'<div class="tip-card">'
                            f'<strong>{item["name"]}:</strong> {item["tip"]}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        shown_tips.add(item["tip"])
                        if len(shown_tips) >= 5:
                            break
                
                # Impact prediction
                st.markdown("#### 🔮 Impact Prediction")
                if total > 0:
                    weekly_est = total * 3  # ~3 grocery trips per week
                    monthly_est = weekly_est * 4.3
                    yearly_est = monthly_est * 12
                    
                    st.markdown(f"If this represents a typical shopping trip:")
                    st.markdown(f"- **Weekly:** ~{weekly_est:.1f} kg CO2e")
                    st.markdown(f"- **Monthly:** ~{monthly_est:.0f} kg CO2e")
                    st.markdown(f"- **Yearly:** ~{yearly_est:.0f} kg CO2e")
                    
                    # Compare to averages
                    avg_canadian_food = 2500  # kg CO2e/year from food
                    pct = (yearly_est / avg_canadian_food) * 100
                    delta_text = "below" if pct < 100 else "above"
                    delta_class = "metric-delta-good" if pct < 100 else "metric-delta-bad"
                    st.markdown(
                        f'<span class="{delta_class}">That\'s {abs(100-pct):.0f}% {delta_text} the Canadian food average</span>',
                        unsafe_allow_html=True,
                    )
        
        # Weekly summary
        if st.session_state.weekly_data:
            st.markdown("---")
            st.markdown("#### 📅 Session History")
            
            weekly_insight = get_weekly_insight(st.session_state.weekly_data)
            st.markdown(
                f'<div class="coach-box">'
                f'<div class="coach-label">📊 Weekly Insight</div>'
                f'{weekly_insight}'
                f'</div>',
                unsafe_allow_html=True,
            )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 6: LEARN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_learn:
    st.markdown("### 📚 Understanding Carbon Footprints")
    
    st.markdown("""
    **What is a carbon footprint?**
    
    Your carbon footprint is the total amount of greenhouse gases (measured in CO2 equivalent) 
    generated by your actions. Everything from the food you eat to how you travel to the energy 
    you use at home contributes to your personal carbon footprint.
    
    **Why does it matter?**
    
    The average person produces about **4.7 tonnes of CO2e per year** globally. To limit warming 
    to 1.5°C (the Paris Agreement target), we need to get to about **2.3 tonnes per person by 2030**. 
    That means most of us need to cut our footprint roughly in half.
    
    **The good news?** Small, informed choices add up. That's what ClimaByte is for.
    """)
    
    st.markdown("---")
    st.markdown("#### 🥩 vs 🥦 Food Carbon Comparison")
    
    # Food comparison chart
    food_compare = []
    highlight_foods = [
        "beef", "lamb", "shrimp", "cheese", "pork", "chicken", "fish", "eggs",
        "rice", "tofu", "pasta", "bread", "beans", "lentils", "potatoes", "bananas"
    ]
    for key in highlight_foods:
        if key in FOOD_EMISSIONS:
            food_compare.append({
                "Food": key.title(),
                "kg CO2e per kg": FOOD_EMISSIONS[key]["co2e_per_kg"],
                "Category": FOOD_EMISSIONS[key]["category"],
            })
    
    fig_food = px.bar(
        food_compare, x="Food", y="kg CO2e per kg", color="Category",
        color_discrete_sequence=["#ff6b6b", "#ffd166", "#00d4aa", "#00b4d8", "#48cae4", "#c77dff"],
        title="Carbon Footprint of Common Foods (kg CO2e per kg)",
        height=400,
    )
    fig_food.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#8ba3c4",
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig_food, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 🔑 Top 5 Things You Can Do")
    
    actions = [
        ("Eat less beef and dairy", "Swapping beef for chicken just once a week saves ~250 kg CO2e/year. Going plant-based for that meal saves even more."),
        ("Drive less, or go electric", "If your commute is under 5km, cycling or transit cuts transport emissions by 80-100%."),
        ("Switch to green energy", "Choosing a renewable electricity provider can eliminate ~1-2 tonnes CO2e/year for most households."),
        ("Reduce food waste", "~30% of food is wasted globally. Planning meals and using leftovers has a real impact."),
        ("Buy less, choose well", "A single pair of jeans = 33 kg CO2e. Buying quality that lasts and shopping second-hand matters."),
    ]
    
    for i, (title, desc) in enumerate(actions, 1):
        st.markdown(f"**{i}. {title}**")
        st.markdown(f"_{desc}_")
    
    st.markdown("---")
    st.markdown("""
    #### 📊 Data Sources
    
    ClimaByte uses emission factors from:
    - **Climatiq API** — Open Emission Factor Database (OEFDB)
    - **EPA** — US Environmental Protection Agency  
    - **DEFRA** — UK Department for Environment, Food & Rural Affairs
    - **Our World in Data** — Peer-reviewed lifecycle analyses
    - **IPCC** — Intergovernmental Panel on Climate Change
    """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BOTTOM: CART DISPLAY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if st.session_state.cart:
    st.markdown("---")
    st.markdown("### 🛒 Your Carbon Cart")
    
    col_cart, col_actions = st.columns([3, 1])
    
    with col_cart:
        for i, item in enumerate(st.session_state.cart):
            col_info, col_co2, col_del = st.columns([3, 1, 0.5])
            with col_info:
                st.markdown(f"**{item['name']}** — {item['quantity']} {item['unit']}")
            with col_co2:
                st.markdown(f"**{item['co2e_total']:.2f}** kg CO2e")
            with col_del:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.total_tracked -= item["co2e_total"]
                    st.session_state.cart.pop(i)
                    st.rerun()
    
    with col_actions:
        total = get_cart_total()
        st.markdown(f"### Total: {total:.2f} kg CO2e")
        
        eq = get_equivalencies(total)
        st.markdown(f"🚗 {eq['driving_km']} km driving")
        st.markdown(f"🌳 {eq['trees_to_offset']} trees (1yr)")
        
        if st.button("Save & Clear Cart", type="primary", key="clear_cart"):
            clear_cart()
            st.rerun()
