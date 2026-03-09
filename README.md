# 🌍 ClimaByte — AI-Powered Personal Carbon Footprint Tracker

**Frostbyte Hackathon 2026 | Sustainability & Climate Tech**

ClimaByte makes understanding your carbon footprint as easy as taking a photo of your grocery receipt. Powered by Claude AI's computer vision and a comprehensive emission factor database, it turns your everyday purchases into actionable climate insights.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Claude AI](https://img.shields.io/badge/Claude-Sonnet%203.5-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 What It Does

1. **📸 Scan Receipts** — Upload a photo of your grocery receipt and Claude Vision extracts every item, calculates the carbon footprint, and adds it to your tracker
2. **🛒 Manual Tracking** — Search or browse 80+ food items with real emission data
3. **🚗 Transport Tracker** — Log commutes and trips across 15 transport modes with instant comparisons
4. **🏠 Home Energy** — Track electricity and heating by source (including Quebec's near-zero hydro grid!)
5. **🤖 AI Climate Coach** — Get personalized, encouraging tips from Claude on how to reduce your impact
6. **📈 Visual Dashboard** — Interactive Plotly charts showing breakdown by category, item, and over time
7. **📚 Learn** — Educational content with food comparisons, top actions, and data sources

## 💡 Why ClimaByte?

Most people want to reduce their carbon footprint but have no idea where to start. ClimaByte bridges the knowledge gap:

- **See the impact** of every purchase in kg CO2e
- **Compare alternatives** — "What if I swapped beef for chicken?"
- **Get coached** by AI that's encouraging, not preachy
- **Track progress** over time with beautiful visualizations

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Language** | Python 3.12 | Fast, huge AI ecosystem, hackathon-ready |
| **Frontend** | Streamlit | Beautiful web UI from pure Python in hours |
| **AI Brain** | Anthropic Claude API (claude-sonnet-4-6) | Multimodal vision + structured output + natural coaching |
| **Carbon Data** | Built-in DB (80+ items) from EPA, DEFRA, Climatiq OEFDB | Real-world emission factors, no made-up numbers |
| **Charts** | Plotly Express | Interactive, beautiful, responsive charts |
| **Image Processing** | Pillow (PIL) | Receipt photo handling before Claude Vision |
| **HTTP** | requests | Clean API calls to Claude and Climatiq |
| **Secrets** | Streamlit secrets + python-dotenv | Zero risk of key leaks |
| **Deployment** | Streamlit Community Cloud | Free, instant, public URL |

**Total cost: $0** — Everything runs on free tiers.

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/limem01/climabyte.git
cd climabyte

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Add your API key (optional — app works without it, just no receipt scanning)
# Edit .streamlit/secrets.toml and add your Anthropic API key

# Run
streamlit run app.py
```

The app opens at `http://localhost:8501`

## 🔑 API Keys

| Key | Required? | Get it at |
|-----|-----------|-----------|
| Anthropic Claude | Optional (enables receipt scanning + AI coaching) | [console.anthropic.com](https://console.anthropic.com/) |
| Climatiq | Optional (enhances emission data) | [app.climatiq.io](https://app.climatiq.io/) |

The app works fully without any API keys using the built-in emission factor database. Keys unlock AI-powered features.

## 📊 Data Sources

All emission factors come from peer-reviewed, authoritative sources:

- **Climatiq OEFDB** — Open Emission Factor Database
- **EPA** — US Environmental Protection Agency
- **DEFRA** — UK Department for Environment, Food & Rural Affairs
- **Our World in Data** — Lifecycle analyses from Oxford/OWID
- **IPCC** — Intergovernmental Panel on Climate Change AR6

## 🏗️ How We Built It

ClimaByte was built in 7 days for the Frostbyte Hackathon 2026. The core insight: people can't change what they can't measure. We combined Claude AI's vision capabilities with comprehensive carbon data to create a tool that makes the invisible visible.

**Architecture:**
1. **Receipt scanning** — Upload photo → Claude Vision extracts items as structured JSON → matched against our emission database → instant carbon calculation
2. **Carbon engine** — 80+ food items, 15 transport modes, 9 energy sources, all with real kg CO2e values from EPA/DEFRA/Climatiq
3. **AI coaching** — Cart data sent to Claude with a carefully crafted system prompt that produces encouraging, specific, actionable advice
4. **Visualization** — Plotly charts update in real-time: pie charts for category breakdown, bar charts for item comparison, country benchmarks

**Key decisions:**
- Built-in emission data (not API-only) so the app always works, even offline
- Claude claude-sonnet-4-6 for the perfect balance of speed, intelligence, and cost
- Streamlit for rapid prototyping — production-quality UI in Python
- Session-based storage for hackathon simplicity (Firebase planned for v2)

## 🔮 What's Next

- [ ] Firebase/Supabase persistent storage for long-term tracking
- [ ] Weekly/monthly progress reports via email
- [ ] Barcode scanning for packaged products
- [ ] Household mode (track family footprint)
- [ ] Carbon offset marketplace integration
- [ ] Mobile PWA wrapper
- [ ] Social features — compare with friends, community challenges

## 📝 License

MIT License — see [LICENSE](LICENSE)

## 👤 Author

**Khalil Limem** — Full-stack developer passionate about using AI to solve real-world problems.

- Email: khalillimem@outlook.com
- GitHub: [@limem01](https://github.com/limem01)

---

*Built with 🌍 for the Frostbyte Hackathon 2026*
