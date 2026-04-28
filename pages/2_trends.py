import streamlit as st
from modules.processor import process_data
import plotly.express as px
import pandas as pd
from utils import apply_theme

@st.cache_data
def load_data():
    return process_data()

st.set_page_config(layout="wide", page_title="Trends and Insights")

# ── THEME ──────────────────────────────────────────────────
theme_option = st.sidebar.selectbox("Select Theme", ["Light", "Dark"], index=0)
apply_theme(theme_option)
is_dark = theme_option == "Dark"

# ── STRONG CSS (VISIBLE CHANGE + ANIMATION) ────────────────
st.markdown(f"""
<style>

/* Background */
body, .stApp {{
    background: {"linear-gradient(135deg, #0f172a, #1e293b)" if is_dark else "linear-gradient(135deg, #e0f2ff, #ffffff)"};
    color: {"white" if is_dark else "#0f172a"};
    transition: all 0.4s ease;
}}

/* Title Animation */
.title {{
    font-size: 2.8rem;
    font-weight: bold;
    text-align: center;
    background: {"linear-gradient(90deg,#6366f1,#22d3ee)" if is_dark else "linear-gradient(90deg,#2563eb,#38bdf8)"};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeIn 1s ease-in-out;
}}

@keyframes fadeIn {{
    from {{opacity:0; transform: translateY(20px);}}
    to {{opacity:1; transform: translateY(0);}}
}}

/* Card Widgets */
.card {{
    padding: 20px;
    border-radius: 15px;
    background: {"rgba(255,255,255,0.05)" if is_dark else "white"};
    border: 1px solid {"rgba(255,255,255,0.1)" if is_dark else "rgba(0,0,0,0.05)"};
    box-shadow: {"none" if is_dark else "0 5px 20px rgba(0,0,0,0.08)"};
    margin-bottom: 15px;
    transition: 0.3s;
}}

.card:hover {{
    transform: translateY(-5px);
}}

/* Chart Box */
.chart-box {{
    padding: 15px;
    border-radius: 15px;
    background: {"rgba(255,255,255,0.04)" if is_dark else "rgba(255,255,255,0.9)"};
    border: 1px solid {"rgba(255,255,255,0.08)" if is_dark else "rgba(0,0,0,0.05)"};
}}

/* Divider */
hr {{
    border: none;
    height: 1px;
    background: {"linear-gradient(to right, transparent, #6366f1, transparent)" if is_dark else "linear-gradient(to right, transparent, #3b82f6, transparent)"};
    margin: 30px 0;
}}

</style>
""", unsafe_allow_html=True)

# ── TITLE ─────────────────────────────────────────────────
st.markdown('<div class="title">📊 Trends & Insights</div>', unsafe_allow_html=True)

st.markdown("### 🔍 Understand your health patterns through data")

st.markdown("---")

# ── LOAD DATA ─────────────────────────────────────────────
with st.spinner('⚡ Processing your data...'):
    df = load_data()

# ── FILTERS ───────────────────────────────────────────────
st.sidebar.header("⚙️ Filters")

time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

if time_range == "Last 7 Days":
    filtered_df = df.sort_values(by='date', ascending=False).head(7)
elif time_range == "Last 30 Days":
    filtered_df = df.sort_values(by='date', ascending=False).head(30)
else:
    filtered_df = df

# ── SUMMARY CARDS ─────────────────────────────────────────
st.markdown("## 📌 Summary Snapshot")

col1, col2, col3 = st.columns(3)

col1.markdown(f'<div class="card">🚶 Steps Avg<br><b>{filtered_df["steps"].mean():.0f}</b></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card">🛌 Sleep Avg<br><b>{filtered_df["sleep_hours"].mean():.1f} hrs</b></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card">⚡ Recovery Avg<br><b>{filtered_df["Recovery_score"].mean():.1f}</b></div>', unsafe_allow_html=True)

st.markdown("---")

# ── TABLE ────────────────────────────────────────────────
st.markdown("## 📋 Detailed Statistics")

st.dataframe(
    filtered_df[['Recovery_score', 'sleep_hours', 'steps', 'calories_burned']].describe().transpose(),
    use_container_width=True
)

st.markdown("---")

# ── LINE CHART ────────────────────────────────────────────
st.markdown("## 📈 Monthly Recovery Trend")

df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
monthly_avg_recovery = df.groupby('month')['Recovery_score'].mean().reset_index()
monthly_avg_recovery['month'] = monthly_avg_recovery['month'].astype(str)

fig1 = px.line(
    monthly_avg_recovery,
    x='month',
    y='Recovery_score',
    title='Recovery Score Trend'
)

st.markdown('<div class="chart-box">', unsafe_allow_html=True)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ── HISTOGRAMS ───────────────────────────────────────────
st.markdown("## 📊 Distribution Insights")

metrics = ['steps', 'calories_burned', 'Recovery_score', 'sleep_hours']

for metric in metrics:
    st.markdown(f"### 📌 {metric.replace('_',' ').title()}")

    fig = px.histogram(filtered_df, x=metric, nbins=30)

    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")