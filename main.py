import streamlit as st 
from modules.processor import load_data, calculate_recovery_score

# Load data
df = load_data()
df = calculate_recovery_score(df)

st.set_page_config(layout="wide", page_title="FitSync", page_icon="⚡")

# ── THEME STATE ─────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

is_dark = st.session_state.theme == "dark"

# ── CSS (YOUR ORIGINAL + LIGHT FIX) ─────────────────────────
CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

/* FIX TOP SPACE */
.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}}

/* BACKGROUND */
body, .stApp {{
    background: {"linear-gradient(135deg, #0f172a, #1e293b)" if is_dark else "#f8fbff"};
    color: {"white" if is_dark else "#0f172a"};
    font-family: 'Poppins', sans-serif;
}}

/* HERO BOX */
.hero-box {{
    text-align: center;
    padding: 70px 40px;
    border-radius: 20px;
    background: {"linear-gradient(135deg, rgba(99,102,241,0.15), rgba(34,211,238,0.15))" if is_dark else "rgba(255,255,255,0.9)"};
    border: {"1px solid rgba(255,255,255,0.1)" if is_dark else "1px solid rgba(0,0,0,0.05)"};
    backdrop-filter: blur(20px);
    box-shadow: {"0 0 40px rgba(99,102,241,0.25)" if is_dark else "0 8px 30px rgba(0,0,0,0.08)"};
    max-width: 900px;
    margin: auto;
    margin-top: 40px;
}}

/* BADGE */
.hero-badge {{
    display: inline-block;
    padding: 15px 35px;
    border-radius: 40px;
    font-weight: bold;
    background: {"linear-gradient(90deg, #6366f1, #22d3ee)" if is_dark else "linear-gradient(90deg, #2563eb, #38bdf8)"};
    box-shadow: 0 5px 20px rgba(99,102,241,0.5);
    margin-bottom: 25px;
}}

/* TITLE */
.hero-title {{
    font-size: 4rem;
    font-weight: 700;
    background: {"linear-gradient(90deg, #6366f1, #22d3ee)" if is_dark else "linear-gradient(90deg, #2563eb, #38bdf8)"};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

/* TEXT */
.hero-sub {{
    font-size: 1.2rem;
    color: {"#cbd5e1" if is_dark else "#475569"};
    max-width: 700px;
    margin: auto;
    line-height: 1.6;
}}

/* CARDS */
.metric-card {{
    background: {"rgba(255,255,255,0.05)" if is_dark else "white"};
    backdrop-filter: blur(15px);
    border-radius: 16px;
    padding: 25px;
    margin: 10px 0;
    border: {"1px solid rgba(255,255,255,0.1)" if is_dark else "1px solid rgba(0,0,0,0.05)"};
    box-shadow: {"none" if is_dark else "0 4px 15px rgba(0,0,0,0.05)"};
    transition: all 0.3s ease;
}}

.metric-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 10px 25px rgba(99,102,241,0.3);
}}

/* TEXT */
.card-title {{
    font-size: 1.2rem;
    font-weight: 600;
}}

.card-desc {{
    color: {"#94a3b8" if is_dark else "#475569"};
}}

/* DIVIDER */
.hr {{
    height: 1px;
    background: {"linear-gradient(to right, transparent, #6366f1, transparent)" if is_dark else "linear-gradient(to right, transparent, #3b82f6, transparent)"};
    margin: 50px 0;
    border: none;
}}

/* HIDE DEFAULT */
header, footer {{visibility: hidden;}}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ── THEME BUTTON ───────────────────────────────────────────
_, btn_col = st.columns([9,1])
with btn_col:
    st.button("🌙" if is_dark else "☀️", on_click=toggle_theme)

# ── HERO SECTION ───────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-badge">⚡ AI Powered Fitness Dashboard</div>
    <div class="hero-title">FitSync</div>
    <div class="hero-sub">
        Your all-in-one intelligent fitness system to track, analyze, and improve your health using smart insights.
        <br><br>
        Transform your daily activity into meaningful data, optimize your performance, and build a healthier lifestyle.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── FEATURES ───────────────────────────────────────────────
features = [
    ("🏋️ Smart Workout Tracking", "Analyze performance trends and improve your workouts."),
    ("🥗 Nutrition Intelligence", "Track food habits and optimize your diet."),
    ("🛌 Sleep & Recovery", "Understand sleep patterns and recovery scores."),
    ("❤️ Health Monitoring", "Track vitals and overall wellness."),
    ("📊 Visual Analytics", "Interactive charts to monitor progress."),
    ("🎯 Goal Tracking", "Build consistent healthy habits.")
]

cols = st.columns(2)

for i, (title, desc) in enumerate(features):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── WHY SECTION ────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;">
    <h2>Why FitSync?</h2>
    <p style="color:#94a3b8; max-width:600px; margin:auto;">
        FitSync transforms your raw fitness data into meaningful insights,
        helping you make smarter decisions and stay consistent.
    </p>
</div>
""", unsafe_allow_html=True)

# ── FINAL TIP ──────────────────────────────────────────────
st.markdown("""
<div class="metric-card" style="text-align:center;">
💡 Connect wearable devices for real-time health tracking.
</div>
""", unsafe_allow_html=True)