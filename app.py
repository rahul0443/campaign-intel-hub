import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Campaign Intelligence Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Hide default streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero header */
.hero-header {
    background: linear-gradient(135deg, #0A0E17 0%, #1a1f35 50%, #0d1a2d 100%);
    border: 1px solid rgba(6, 214, 160, 0.15);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(6, 214, 160, 0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 36px;
    font-weight: 800;
    background: linear-gradient(135deg, #06D6A0, #48e8c5, #06D6A0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-family: 'Outfit', sans-serif;
    font-size: 15px;
    color: #8892a4;
    margin-top: 6px;
    font-weight: 400;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(145deg, #131A2B, #0f1525);
    border: 1px solid rgba(6, 214, 160, 0.1);
    border-radius: 14px;
    padding: 22px 24px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-card:hover {
    border-color: rgba(6, 214, 160, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(6, 214, 160, 0.08);
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 32px;
    font-weight: 700;
    color: #06D6A0;
    margin: 0;
    line-height: 1.1;
}
.metric-label {
    font-family: 'Outfit', sans-serif;
    font-size: 12px;
    color: #6b7689;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 8px;
    font-weight: 500;
}
.metric-delta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    margin-top: 6px;
    font-weight: 600;
}
.delta-up { color: #06D6A0; }
.delta-down { color: #EF476F; }

/* Section headers */
.section-header {
    font-family: 'Outfit', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #E8ECF1;
    margin: 32px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(6, 214, 160, 0.2);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Anomaly card */
.anomaly-card {
    background: linear-gradient(145deg, #1a0a0f, #1f1020);
    border: 1px solid rgba(239, 71, 111, 0.25);
    border-left: 4px solid #EF476F;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.anomaly-card.warning {
    background: linear-gradient(145deg, #1a1508, #1f1a10);
    border: 1px solid rgba(255, 209, 102, 0.25);
    border-left: 4px solid #FFD166;
}
.anomaly-name {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 14px;
    color: #E8ECF1;
}
.anomaly-detail {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #8892a4;
    margin-top: 4px;
}

/* AI insight box */
.ai-insight-box {
    background: linear-gradient(145deg, #0d1a2d, #101f30);
    border: 1px solid rgba(6, 214, 160, 0.2);
    border-radius: 14px;
    padding: 24px 28px;
    margin: 16px 0;
    position: relative;
}
.ai-insight-box::before {
    content: '🤖';
    position: absolute;
    top: -12px;
    left: 20px;
    font-size: 20px;
    background: #0A0E17;
    padding: 0 8px;
}
.ai-insight-title {
    font-family: 'Outfit', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #06D6A0;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}
.ai-insight-text {
    font-family: 'Outfit', sans-serif;
    font-size: 14px;
    color: #c8ced8;
    line-height: 1.7;
}

/* Health badge */
.health-critical { 
    background: rgba(239, 71, 111, 0.15); 
    color: #EF476F; 
    padding: 4px 12px; 
    border-radius: 20px; 
    font-size: 12px; 
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.health-at-risk { 
    background: rgba(255, 209, 102, 0.15); 
    color: #FFD166; 
    padding: 4px 12px; 
    border-radius: 20px; 
    font-size: 12px; 
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.health-healthy { 
    background: rgba(6, 214, 160, 0.15); 
    color: #06D6A0; 
    padding: 4px 12px; 
    border-radius: 20px; 
    font-size: 12px; 
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: #080c14;
    border-right: 1px solid rgba(6, 214, 160, 0.08);
}
[data-testid="stSidebar"] .stMarkdown h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 18px;
    color: #06D6A0;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 14px;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_demo_data():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "demo_campaign_data.csv"))

def classify_health(row):
    score = row["engagement_score"]
    if score < 30:
        return "Critical"
    elif score < 55:
        return "At Risk"
    else:
        return "Healthy"

def detect_anomalies(df):
    anomalies = []
    for channel in df["channel"].unique():
        ch_df = df[df["channel"] == channel]
        if len(ch_df) < 3:
            continue
        
        ctr_mean = ch_df["ctr"].mean()
        ctr_std = ch_df["ctr"].std()
        conv_mean = ch_df["conversion_rate"].mean()
        conv_std = ch_df["conversion_rate"].std()
        
        for _, row in ch_df.iterrows():
            reasons = []
            severity = "warning"
            
            if ctr_std > 0 and row["ctr"] < ctr_mean - 1.5 * ctr_std:
                reasons.append(f"CTR ({row['ctr']:.2f}%) is {((ctr_mean - row['ctr'])/ctr_mean*100):.0f}% below channel avg")
                severity = "critical"
            
            if conv_std > 0 and row["conversion_rate"] < conv_mean - 1.5 * conv_std:
                reasons.append(f"Conv rate ({row['conversion_rate']:.2f}%) is {((conv_mean - row['conversion_rate'])/conv_mean*100):.0f}% below channel avg")
                severity = "critical"
            
            if row["spend"] > 0 and row["roas"] < 0.5 and row["spend"] > 1000:
                reasons.append(f"ROAS of {row['roas']:.1f}x on ${row['spend']:,.0f} spend")
            
            if row["spend"] > 5000 and row["conversions"] < 3:
                reasons.append(f"Only {row['conversions']} conversions on ${row['spend']:,.0f} spend")
                severity = "critical"
            
            if reasons:
                anomalies.append({
                    "campaign": row["campaign_name"],
                    "channel": row["channel"],
                    "team": row["team"],
                    "reasons": reasons,
                    "severity": severity,
                    "spend": row["spend"],
                    "engagement_score": row["engagement_score"],
                })
    
    return sorted(anomalies, key=lambda x: x["engagement_score"])

def generate_ai_analysis(df, anomalies):
    """Generate AI analysis using GPT-4o if API key available, else use rule-based."""
    
    api_key = os.environ.get("OPENAI_API_KEY", "")
    
    # Prepare context
    total_spend = df["spend"].sum()
    total_revenue = df["revenue_attributed"].sum()
    overall_roas = total_revenue / total_spend if total_spend > 0 else 0
    top_channel = df.groupby("channel")["revenue_attributed"].sum().idxmax()
    worst_channel = df.groupby("channel")["roas"].mean().idxmin()
    critical_count = len([a for a in anomalies if a["severity"] == "critical"])
    
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            summary_data = {
                "total_campaigns": len(df),
                "total_spend": f"${total_spend:,.0f}",
                "total_revenue": f"${total_revenue:,.0f}",
                "overall_roas": f"{overall_roas:.1f}x",
                "top_channel_by_revenue": top_channel,
                "worst_channel_by_roas": worst_channel,
                "critical_anomalies": critical_count,
                "channel_performance": df.groupby("channel").agg({
                    "spend": "sum", "revenue_attributed": "sum", "ctr": "mean", 
                    "conversion_rate": "mean", "roas": "mean"
                }).round(2).to_dict(),
                "anomaly_details": [{"campaign": a["campaign"], "reasons": a["reasons"]} for a in anomalies[:8]],
            }
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a senior marketing operations analyst. Provide a concise, actionable analysis of campaign performance data. Use specific numbers. Be direct and strategic. Format in 3 sections: EXECUTIVE SUMMARY (2-3 sentences), KEY FINDINGS (4-5 bullet points with specific metrics), RECOMMENDED ACTIONS (3-4 specific, implementable actions). Do not use markdown headers, just plain text with bullet points using dashes."},
                    {"role": "user", "content": f"Analyze this marketing campaign data and provide strategic recommendations:\n\n{json.dumps(summary_data, indent=2)}"}
                ],
                max_tokens=800,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            pass
    
    # Fallback: rule-based analysis
    analysis = f"""EXECUTIVE SUMMARY
Across {len(df)} campaigns with ${total_spend:,.0f} total spend, the portfolio generated ${total_revenue:,.0f} in attributed revenue at an overall ROAS of {overall_roas:.1f}x. {critical_count} campaigns are flagged as critical anomalies requiring immediate attention, representing potential budget waste.

KEY FINDINGS
- {top_channel} is the top-performing channel by attributed revenue, driving the highest ROAS across the portfolio
- {worst_channel} is underperforming with the lowest average ROAS across campaigns and should be evaluated for budget reallocation
- {critical_count} campaigns show statistically significant underperformance vs. channel benchmarks (CTR or conversion rate below 1.5 standard deviations)
- {len(df[df['status'] == 'Active'])} campaigns are currently active, with {len(df[(df['status'] == 'Active') & (df['engagement_score'] < 30)])} in critical health status
- Retention-stage campaigns show {df[df['funnel_stage']=='Retention']['roas'].mean():.1f}x ROAS vs. {df[df['funnel_stage']=='Awareness']['roas'].mean():.1f}x for Awareness, suggesting lifecycle investment pays off

RECOMMENDED ACTIONS
- Pause or restructure the {critical_count} critical anomaly campaigns and reallocate ${sum(a['spend'] for a in anomalies if a['severity']=='critical'):,.0f} toward top performers
- Shift 15-20% of {worst_channel} budget to {top_channel} based on ROAS differential
- Implement automated performance alerts for campaigns dropping below 1.0x ROAS threshold within first 7 days of launch
- Build an A/B testing framework for underperforming ad creatives in Paid Social and Display before scaling spend"""
    
    return analysis


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("# ⚡ Campaign Intel Hub")
    st.markdown("---")
    
    data_source = st.radio("Data Source", ["Demo Dataset", "Upload CSV"], index=0)
    
    if data_source == "Upload CSV":
        uploaded = st.file_uploader("Upload campaign data", type=["csv"])
        if uploaded:
            df = pd.read_csv(uploaded)
        else:
            st.info("Upload a CSV with campaign metrics or use the demo dataset.")
            df = load_demo_data()
    else:
        df = load_demo_data()
    
    df["health"] = df.apply(classify_health, axis=1)
    
    st.markdown("### Filters")
    
    quarters = st.multiselect("Quarter", df["quarter"].unique().tolist(), default=df["quarter"].unique().tolist())
    channels = st.multiselect("Channel", df["channel"].unique().tolist(), default=df["channel"].unique().tolist())
    teams = st.multiselect("Team", df["team"].unique().tolist(), default=df["team"].unique().tolist())
    health_filter = st.multiselect("Health Status", ["Healthy", "At Risk", "Critical"], default=["Healthy", "At Risk", "Critical"])
    
    # Apply filters
    mask = (
        df["quarter"].isin(quarters) & 
        df["channel"].isin(channels) & 
        df["team"].isin(teams) &
        df["health"].isin(health_filter)
    )
    filtered_df = df[mask].copy()
    
    st.markdown("---")
    st.markdown(f"**{len(filtered_df)}** campaigns loaded")
    st.markdown(f"Built by [Rahul Muddhapuram](https://github.com/rahul0443)")


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <p class="hero-title">Campaign Intelligence Hub</p>
    <p class="hero-subtitle">AI-powered marketing operations dashboard — anomaly detection, campaign health scoring, and optimization recommendations</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI METRICS ROW
# ─────────────────────────────────────────────
total_spend = filtered_df["spend"].sum()
total_revenue = filtered_df["revenue_attributed"].sum()
overall_roas = total_revenue / total_spend if total_spend > 0 else 0
avg_ctr = filtered_df["ctr"].mean()
avg_conv = filtered_df["conversion_rate"].mean()
total_conversions = filtered_df["conversions"].sum()
critical_count = len(filtered_df[filtered_df["health"] == "Critical"])
healthy_pct = len(filtered_df[filtered_df["health"] == "Healthy"]) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">${total_spend/1000:.0f}K</p>
        <p class="metric-label">Total Spend</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">${total_revenue/1000:.0f}K</p>
        <p class="metric-label">Revenue Attributed</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    roas_color = "#06D6A0" if overall_roas >= 2 else "#FFD166" if overall_roas >= 1 else "#EF476F"
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value" style="color: {roas_color}">{overall_roas:.1f}x</p>
        <p class="metric-label">Overall ROAS</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{avg_ctr:.2f}%</p>
        <p class="metric-label">Avg CTR</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{total_conversions:,}</p>
        <p class="metric-label">Total Conversions</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    health_color = "#06D6A0" if critical_count == 0 else "#EF476F"
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value" style="color: {health_color}">{critical_count}</p>
        <p class="metric-label">Critical Campaigns</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Performance", "🔍 Anomalies", "🤖 AI Analysis", "📋 Campaign Table", "🗺️ Channel Mix"])

# ─── TAB 1: PERFORMANCE ───
with tab1:
    st.markdown('<div class="section-header">📊 Channel Performance Overview</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # ROAS by channel
        channel_perf = filtered_df.groupby("channel").agg({
            "spend": "sum", "revenue_attributed": "sum", "roas": "mean"
        }).reset_index().sort_values("roas", ascending=True)
        
        fig_roas = go.Figure()
        colors = ["#EF476F" if r < 1 else "#FFD166" if r < 2 else "#06D6A0" for r in channel_perf["roas"]]
        fig_roas.add_trace(go.Bar(
            y=channel_perf["channel"], x=channel_perf["roas"],
            orientation="h", marker_color=colors,
            text=[f"{r:.1f}x" for r in channel_perf["roas"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=12),
        ))
        fig_roas.add_vline(x=1, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_roas.update_layout(
            title=dict(text="Avg ROAS by Channel", font=dict(family="Outfit", size=16, color="#E8ECF1")),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8892a4", family="Outfit"),
            height=380, margin=dict(l=10, r=60, t=50, b=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title=""),
            yaxis=dict(showgrid=False, title=""),
        )
        st.plotly_chart(fig_roas, use_container_width=True)
    
    with col_right:
        # Spend vs Revenue scatter
        channel_scatter = filtered_df.groupby("channel").agg({
            "spend": "sum", "revenue_attributed": "sum", "conversions": "sum"
        }).reset_index()
        
        fig_scatter = px.scatter(
            channel_scatter, x="spend", y="revenue_attributed", size="conversions",
            color="channel", text="channel",
            color_discrete_sequence=["#06D6A0", "#48e8c5", "#FFD166", "#EF476F", "#118AB2", "#073B4C", "#8338EC", "#FF6B6B"],
        )
        fig_scatter.update_traces(textposition="top center", textfont=dict(size=10, family="Outfit"))
        fig_scatter.update_layout(
            title=dict(text="Spend vs Revenue by Channel", font=dict(family="Outfit", size=16, color="#E8ECF1")),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8892a4", family="Outfit"),
            height=380, margin=dict(l=10, r=10, t=50, b=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Total Spend ($)", tickprefix="$"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Revenue Attributed ($)", tickprefix="$"),
            showlegend=False,
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Funnel stage performance
    st.markdown('<div class="section-header">🎯 Funnel Stage Performance</div>', unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        funnel_data = filtered_df.groupby("funnel_stage").agg({
            "spend": "sum", "conversions": "sum", "roas": "mean", "ctr": "mean"
        }).reset_index()
        
        stage_order = ["Awareness", "Consideration", "Decision", "Retention"]
        funnel_data["funnel_stage"] = pd.Categorical(funnel_data["funnel_stage"], categories=stage_order, ordered=True)
        funnel_data = funnel_data.sort_values("funnel_stage")
        
        fig_funnel = go.Figure()
        fig_funnel.add_trace(go.Bar(
            x=funnel_data["funnel_stage"], y=funnel_data["spend"],
            name="Spend", marker_color="#118AB2", opacity=0.7,
        ))
        fig_funnel.add_trace(go.Bar(
            x=funnel_data["funnel_stage"], y=funnel_data["conversions"] * 50,
            name="Conversions (scaled)", marker_color="#06D6A0", opacity=0.7,
        ))
        fig_funnel.update_layout(
            title=dict(text="Spend & Conversions by Funnel Stage", font=dict(family="Outfit", size=16, color="#E8ECF1")),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8892a4", family="Outfit"),
            height=350, margin=dict(l=10, r=10, t=50, b=10),
            barmode="group", showlegend=True,
            legend=dict(font=dict(size=11)),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title=""),
        )
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    with col_f2:
        # Health distribution
        health_counts = filtered_df["health"].value_counts()
        colors_map = {"Healthy": "#06D6A0", "At Risk": "#FFD166", "Critical": "#EF476F"}
        
        fig_health = go.Figure(data=[go.Pie(
            labels=health_counts.index, values=health_counts.values,
            marker=dict(colors=[colors_map.get(h, "#888") for h in health_counts.index]),
            hole=0.6, textinfo="label+percent",
            textfont=dict(family="Outfit", size=13),
        )])
        fig_health.update_layout(
            title=dict(text="Campaign Health Distribution", font=dict(family="Outfit", size=16, color="#E8ECF1")),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8892a4", family="Outfit"),
            height=350, margin=dict(l=10, r=10, t=50, b=10),
            showlegend=False,
            annotations=[dict(text=f"{healthy_pct:.0f}%<br>Healthy", x=0.5, y=0.5, font=dict(size=18, family="JetBrains Mono", color="#06D6A0"), showarrow=False)],
        )
        st.plotly_chart(fig_health, use_container_width=True)

# ─── TAB 2: ANOMALIES ───
with tab2:
    st.markdown('<div class="section-header">🔍 Anomaly Detection Engine</div>', unsafe_allow_html=True)
    st.markdown("Campaigns flagged by statistical deviation from channel benchmarks (CTR or conversion rate > 1.5σ below mean) and ROAS thresholds.")
    
    anomalies = detect_anomalies(filtered_df)
    
    if anomalies:
        critical_anomalies = [a for a in anomalies if a["severity"] == "critical"]
        warning_anomalies = [a for a in anomalies if a["severity"] == "warning"]
        
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            st.markdown(f"**{len(critical_anomalies)} Critical** | **{len(warning_anomalies)} Warning**")
            
            for a in anomalies[:12]:
                css_class = "anomaly-card" if a["severity"] == "critical" else "anomaly-card warning"
                severity_icon = "🔴" if a["severity"] == "critical" else "🟡"
                reasons_html = "<br>".join([f"&bull; {r}" for r in a["reasons"]])
                
                st.markdown(f"""
                <div class="{css_class}">
                    <div class="anomaly-name">{severity_icon} {a['campaign']}</div>
                    <div class="anomaly-detail">{a['channel']} | {a['team']} | Score: {a['engagement_score']:.0f}/100</div>
                    <div class="anomaly-detail" style="margin-top:6px">{reasons_html}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_b:
            # Anomaly scatter plot
            anom_df = pd.DataFrame(anomalies)
            
            fig_anom = px.scatter(
                filtered_df, x="ctr", y="conversion_rate", size="spend",
                color="health",
                color_discrete_map={"Healthy": "#06D6A0", "At Risk": "#FFD166", "Critical": "#EF476F"},
                hover_data=["campaign_name", "channel", "spend", "roas"],
                opacity=0.7,
            )
            fig_anom.update_layout(
                title=dict(text="CTR vs Conversion Rate (size = spend)", font=dict(family="Outfit", size=16, color="#E8ECF1")),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8892a4", family="Outfit"),
                height=500, margin=dict(l=10, r=10, t=50, b=10),
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="CTR (%)"),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Conversion Rate (%)"),
                legend=dict(title="Health", font=dict(size=12)),
            )
            st.plotly_chart(fig_anom, use_container_width=True)
            
            # Wasted spend
            wasted = sum(a["spend"] for a in critical_anomalies)
            st.markdown(f"""
            <div class="metric-card" style="border-color: rgba(239,71,111,0.3)">
                <p class="metric-value" style="color: #EF476F">${wasted:,.0f}</p>
                <p class="metric-label">Spend at Risk (Critical Campaigns)</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No anomalies detected. All campaigns are performing within expected ranges.")

# ─── TAB 3: AI ANALYSIS ───
with tab3:
    st.markdown('<div class="section-header">🤖 AI-Powered Campaign Analysis</div>', unsafe_allow_html=True)
    
    anomalies_for_ai = detect_anomalies(filtered_df)
    
    if st.button("Generate AI Analysis", type="primary", use_container_width=True):
        with st.spinner("Analyzing campaign data..."):
            analysis = generate_ai_analysis(filtered_df, anomalies_for_ai)
        
        st.markdown(f"""
        <div class="ai-insight-box">
            <div class="ai-insight-title">Campaign Intelligence Report</div>
            <div class="ai-insight-text">{analysis.replace(chr(10), '<br>')}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Click 'Generate AI Analysis' to get GPT-4o powered insights on your campaign portfolio. If no API key is set, a rule-based analysis will be generated.")
    
    # Quick stats for context
    st.markdown('<div class="section-header">📈 Analysis Context</div>', unsafe_allow_html=True)
    
    col_ctx1, col_ctx2, col_ctx3 = st.columns(3)
    
    with col_ctx1:
        top_by_roas = filtered_df.nlargest(5, "roas")[["campaign_name", "channel", "roas", "spend"]].reset_index(drop=True)
        top_by_roas.columns = ["Campaign", "Channel", "ROAS", "Spend"]
        top_by_roas["ROAS"] = top_by_roas["ROAS"].apply(lambda x: f"{x:.1f}x")
        top_by_roas["Spend"] = top_by_roas["Spend"].apply(lambda x: f"${x:,.0f}")
        st.markdown("**Top 5 by ROAS**")
        st.dataframe(top_by_roas, use_container_width=True, hide_index=True)
    
    with col_ctx2:
        bottom_by_roas = filtered_df[filtered_df["spend"] > 500].nsmallest(5, "roas")[["campaign_name", "channel", "roas", "spend"]].reset_index(drop=True)
        bottom_by_roas.columns = ["Campaign", "Channel", "ROAS", "Spend"]
        bottom_by_roas["ROAS"] = bottom_by_roas["ROAS"].apply(lambda x: f"{x:.1f}x")
        bottom_by_roas["Spend"] = bottom_by_roas["Spend"].apply(lambda x: f"${x:,.0f}")
        st.markdown("**Bottom 5 by ROAS (> $500 spend)**")
        st.dataframe(bottom_by_roas, use_container_width=True, hide_index=True)
    
    with col_ctx3:
        team_perf = filtered_df.groupby("team").agg({"roas": "mean", "spend": "sum"}).round(2).reset_index()
        team_perf.columns = ["Team", "Avg ROAS", "Total Spend"]
        team_perf["Avg ROAS"] = team_perf["Avg ROAS"].apply(lambda x: f"{x:.1f}x")
        team_perf["Total Spend"] = team_perf["Total Spend"].apply(lambda x: f"${x:,.0f}")
        team_perf = team_perf.sort_values("Avg ROAS", ascending=False)
        st.markdown("**Team Performance**")
        st.dataframe(team_perf, use_container_width=True, hide_index=True)

# ─── TAB 4: CAMPAIGN TABLE ───
with tab4:
    st.markdown('<div class="section-header">📋 Campaign Details</div>', unsafe_allow_html=True)
    
    display_cols = [
        "campaign_name", "channel", "funnel_stage", "team", "status", "health",
        "spend", "impressions", "clicks", "ctr", "conversions", "conversion_rate",
        "roas", "revenue_attributed", "engagement_score"
    ]
    
    sort_by = st.selectbox("Sort by", ["engagement_score", "roas", "spend", "ctr", "conversion_rate", "revenue_attributed"], index=0)
    sort_order = st.radio("Order", ["Ascending", "Descending"], index=1, horizontal=True)
    
    sorted_df = filtered_df[display_cols].sort_values(sort_by, ascending=(sort_order == "Ascending"))
    
    st.dataframe(
        sorted_df,
        use_container_width=True,
        hide_index=True,
        height=500,
        column_config={
            "campaign_name": st.column_config.TextColumn("Campaign", width="large"),
            "channel": "Channel",
            "funnel_stage": "Stage",
            "team": "Team",
            "status": "Status",
            "health": "Health",
            "spend": st.column_config.NumberColumn("Spend", format="$%.0f"),
            "impressions": st.column_config.NumberColumn("Impressions", format="%d"),
            "clicks": st.column_config.NumberColumn("Clicks", format="%d"),
            "ctr": st.column_config.NumberColumn("CTR %", format="%.2f%%"),
            "conversions": st.column_config.NumberColumn("Conv", format="%d"),
            "conversion_rate": st.column_config.NumberColumn("Conv %", format="%.2f%%"),
            "roas": st.column_config.NumberColumn("ROAS", format="%.1fx"),
            "revenue_attributed": st.column_config.NumberColumn("Revenue", format="$%.0f"),
            "engagement_score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%.0f"),
        }
    )

# ─── TAB 5: CHANNEL MIX ───
with tab5:
    st.markdown('<div class="section-header">🗺️ Channel Mix & Budget Allocation</div>', unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        # Spend allocation treemap
        channel_spend = filtered_df.groupby(["channel", "funnel_stage"]).agg({"spend": "sum"}).reset_index()
        
        fig_tree = px.treemap(
            channel_spend, path=["channel", "funnel_stage"], values="spend",
            color="spend", color_continuous_scale=["#0d1a2d", "#118AB2", "#06D6A0"],
        )
        fig_tree.update_layout(
            title=dict(text="Budget Allocation by Channel & Stage", font=dict(family="Outfit", size=16, color="#E8ECF1")),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E8ECF1", family="Outfit"),
            height=420, margin=dict(l=10, r=10, t=50, b=10),
            coloraxis_showscale=False,
        )
        fig_tree.update_traces(textfont=dict(family="Outfit", size=13))
        st.plotly_chart(fig_tree, use_container_width=True)
    
    with col_m2:
        # Quarter over quarter trend
        qoq = filtered_df.groupby(["quarter", "channel"]).agg({"spend": "sum", "roas": "mean"}).reset_index()
        
        fig_qoq = px.bar(
            qoq, x="quarter", y="spend", color="channel", barmode="stack",
            color_discrete_sequence=["#06D6A0", "#48e8c5", "#FFD166", "#EF476F", "#118AB2", "#073B4C", "#8338EC", "#FF6B6B"],
        )
        fig_qoq.update_layout(
            title=dict(text="Spend by Quarter & Channel", font=dict(family="Outfit", size=16, color="#E8ECF1")),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8892a4", family="Outfit"),
            height=420, margin=dict(l=10, r=10, t=50, b=10),
            xaxis=dict(showgrid=False, title=""), yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Spend ($)", tickprefix="$"),
            legend=dict(font=dict(size=10)),
        )
        st.plotly_chart(fig_qoq, use_container_width=True)
    
    # Efficiency matrix
    st.markdown('<div class="section-header">⚡ Channel Efficiency Matrix</div>', unsafe_allow_html=True)
    
    eff_data = filtered_df.groupby("channel").agg({
        "ctr": "mean", "conversion_rate": "mean", "roas": "mean", 
        "spend": "sum", "conversions": "sum", "cpa": "mean"
    }).reset_index().round(2)
    
    fig_eff = px.scatter(
        eff_data, x="cpa", y="roas", size="spend", text="channel",
        color="roas",
        color_continuous_scale=["#EF476F", "#FFD166", "#06D6A0"],
    )
    fig_eff.update_traces(textposition="top center", textfont=dict(size=12, family="Outfit", color="#E8ECF1"))
    fig_eff.update_layout(
        title=dict(text="CPA vs ROAS (size = total spend)", font=dict(family="Outfit", size=16, color="#E8ECF1")),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8892a4", family="Outfit"),
        height=400, margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Avg CPA ($)", tickprefix="$"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Avg ROAS"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_eff, use_container_width=True)
