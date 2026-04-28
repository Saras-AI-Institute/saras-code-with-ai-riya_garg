import plotly.express as px
import streamlit as st
from utils import apply_theme
from modules.processor import process_data

@st.cache_data
def load_data():
    return process_data()

st.set_page_config(layout="wide", page_title="Dashboard")

# ── THEME SELECTION ────────────────────────────────────────
theme_option = st.sidebar.selectbox("Select Theme", ["Light", "Dark"], index=0)
apply_theme(theme_option)

# ── CSS THEMES ─────────────────────────────────────────────

DARK_CSS = """
<style>
body, .stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Header */
.dashboard-title {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Cards */
.metric-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(99,102,241,0.3);
}

/* Chart container */
.chart-box {
    background: rgba(255,255,255,0.04);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Divider */
.hr {
    height: 1px;
    background: linear-gradient(to right, transparent, #6366f1, transparent);
    margin: 30px 0;
}
</style>
"""

LIGHT_CSS = """
<style>
body, .stApp {
    background: linear-gradient(135deg, #e0f2ff, #f8fbff);
    color: #0f172a;
}

/* Header */
.dashboard-title {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Cards */
.metric-card {
    background: rgba(255,255,255,0.85);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(37,99,235,0.2);
}

/* Chart container */
.chart-box {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(0,0,0,0.05);
}

/* Divider */
.hr {
    height: 1px;
    background: linear-gradient(to right, transparent, #3b82f6, transparent);
    margin: 30px 0;
}
</style>
"""

# Apply CSS
st.markdown(DARK_CSS if theme_option == "Dark" else LIGHT_CSS, unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────
st.markdown('<div class="dashboard-title">📊 FitSync Dashboard</div>', unsafe_allow_html=True)

st.markdown("""
Track your fitness data through meaningful insights and visual analytics.
""")

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────
df = load_data()

# ── FILTERS ───────────────────────────────────────────────
st.sidebar.header("Filters")

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

# ── METRICS ───────────────────────────────────────────────
avg_steps = filtered_df['steps'].mean()
avg_sleep = filtered_df['sleep_hours'].mean()
avg_recovery = filtered_df['Recovery_score'].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>🚶 Steps</div>
        <h2>{avg_steps:.0f}</h2>
        <small>Average activity level</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>🛌 Sleep</div>
        <h2>{avg_sleep:.1f} hrs</h2>
        <small>Rest & recovery</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>⚡ Recovery</div>
        <h2>{avg_recovery:.1f}</h2>
        <small>Performance readiness</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── CHARTS ROW 1 ──────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("Recovery & Sleep Trend")
    st.caption("Understand how sleep affects your recovery over time.")
    
    fig = px.line(filtered_df, x='date', y=['Recovery_score', 'sleep_hours'])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("Recovery vs Steps")
    st.caption("See how daily activity impacts your recovery score.")
    
    fig = px.scatter(filtered_df, x='steps', y='Recovery_score', color='sleep_hours')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── CHARTS ROW 2 ──────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("Recovery vs Heart Rate")
    st.caption("Higher resting heart rate may indicate lower recovery.")
    
    fig = px.scatter(filtered_df, x='heart_rate_bpm', y='Recovery_score')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("Calories Burned Trend")
    st.caption("Track your daily energy expenditure.")
    
    fig = px.line(filtered_df, x='date', y='calories_burned')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)