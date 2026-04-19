# ⚡ Campaign Intelligence Hub

An AI-powered marketing operations dashboard that ingests campaign data, detects performance anomalies, scores campaign health, and generates optimization recommendations using GPT-4o.

**[Live Demo](https://campaign-intel.streamlit.app)** | Built by [Rahul Muddhapuram](https://github.com/rahul0443)

---

## What It Does

Marketing teams run dozens of campaigns across channels simultaneously. Performance problems hide in spreadsheets until budgets are already burned. This tool surfaces those problems automatically.

| Feature | How It Works |
|---------|-------------|
| **Anomaly Detection** | Statistical deviation analysis (1.5σ) flags campaigns underperforming vs. channel benchmarks |
| **Health Scoring** | Composite engagement score (0-100) classifies campaigns as Healthy, At Risk, or Critical |
| **AI Analysis** | GPT-4o generates executive summaries, key findings, and specific action items from portfolio data |
| **Channel Mix** | Interactive treemaps and efficiency matrices reveal budget allocation and ROAS by channel/stage |
| **Custom Data** | Upload any campaign CSV or explore the built-in demo dataset modeled after HubSpot exports |

---

## Tech Stack

- **Frontend:** Streamlit with custom CSS (dark theme, JetBrains Mono + Outfit typography)
- **Visualization:** Plotly (interactive charts, treemaps, scatter plots)
- **AI Engine:** GPT-4o via OpenAI API (with rule-based fallback)
- **Data Processing:** pandas, NumPy
- **Deployment:** Streamlit Cloud

---

## Quick Start

```bash
git clone https://github.com/rahul0443/campaign-intel-hub.git
cd campaign-intel-hub
pip install -r requirements.txt
streamlit run app.py
```

### Optional: Enable GPT-4o Analysis

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-key-here"
```

Without the key, the AI Analysis tab uses a rule-based engine that still provides actionable insights.

---

## Dashboard Sections

### Performance Overview
Channel ROAS comparison, spend vs. revenue scatter, funnel stage analysis, and campaign health distribution.

### Anomaly Detection
Statistical engine flags campaigns with CTR or conversion rates significantly below channel averages. Each anomaly includes specific reasons, severity classification, and total spend at risk.

### AI Analysis
One-click GPT-4o analysis generates an executive summary, key findings with specific metrics, and recommended budget reallocation actions.

### Campaign Table
Sortable, filterable table with health-scored progress bars. Export-ready for stakeholder reporting.

### Channel Mix
Budget allocation treemaps, quarter-over-quarter spend trends, and a CPA vs. ROAS efficiency matrix.

---

## CSV Format

Upload any CSV with these columns (column names are flexible):

| Column | Description |
|--------|-------------|
| campaign_name | Campaign identifier |
| channel | Marketing channel (Email, Paid Search, etc.) |
| spend | Total spend ($) |
| impressions | Total impressions |
| clicks | Total clicks |
| conversions | Total conversions |
| revenue_attributed | Revenue attributed ($) |

Additional columns (funnel_stage, team, quarter, status) enhance the analysis but are optional.
