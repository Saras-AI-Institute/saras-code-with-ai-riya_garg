import streamlit as st
from modules.processor import load_data, calculate_recovery_score

# Load and process data
df = load_data()
df = calculate_recovery_score(df)

# Set page configuration
st.set_page_config(layout="wide", page_title="FitSync", page_icon="⚡")

# ── Theme state ────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

is_dark = st.session_state.theme == "dark"

# ── CSS themes ─────────────────────────────────────────────────────────────────
DARK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600&family=DM+Sans&display=swap');
    body, .stApp { background-color: #0e153a !important; color: #ffffff; font-family: 'DM Sans', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Syne', sans-serif; color: #00d4ff; margin-bottom: 0; }
    .headline-gradient {
        font-size: 3.7rem;
        background: linear-gradient(120deg, #00f5a0, #00d4ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 25px 0 20px; text-align: center;
    }
    .pill-badge {
        display: block; padding: 12px 30px; border-radius: 25px;
        background-color: #00f5a0; color: #0e153a;
        margin: 20px auto; font-size: 1.1rem; font-weight: bold; text-align: center; width: fit-content;
    }
    .metric-card {
        border-radius: 12px; padding: 25px; background-color: #1f2440;
        color: #ffffff; text-align: center;
        box-shadow: 0 6px 18px rgba(0,0,0,0.2); margin: 15px 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    .metric-card h3 { margin: 15px 0 10px; color: #29abe2; }
    .metric-card .value { font-size: 2.7rem; font-weight: bold; color: #ffffff; }
    .metric-card .label { text-transform: uppercase; font-size: 0.9rem; color: #cccccc; }
    .pro-tip {
        background-color: #1b1b33; padding: 15px; border-radius: 10px;
        display: flex; align-items: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.25); margin-top: 45px; color: #ffffff;
    }
    .pro-tip-icon { margin-right: 12px; font-size: 1.8rem; color: #00f5a0; }
    .sidebar-arrow { animation: bounce 2s infinite; margin: 25px 0; color: #00f5a0; font-size: 2rem; text-align: center; }
    .hr-divider { border: none; height: 1px; background: linear-gradient(90deg, #00f5a0, #00d4ff); margin: 20px 0; }
    footer { display: none; } header { display: none; }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-12px); }
        60% { transform: translateY(-6px); }
    }
</style>
"""

LIGHT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600&family=DM+Sans&display=swap');
    body, .stApp { background-color: #f4f6fb !important; color: #1a1a2e; font-family: 'DM Sans', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Syne', sans-serif; color: #0077b6; margin-bottom: 0; }
    .headline-gradient {
        font-size: 3.7rem;
        background: linear-gradient(120deg, #00a86b, #0077b6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 25px 0 20px; text-align: center;
    }
    .pill-badge {
        display: block; padding: 12px 30px; border-radius: 25px;
        background-color: #0077b6; color: #ffffff;
        margin: 20px auto; font-size: 1.1rem; font-weight: bold; text-align: center; width: fit-content;
    }
    .metric-card {
        border-radius: 12px; padding: 25px; background-color: #ffffff;
        color: #1a1a2e; text-align: center;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08); margin: 15px 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.12); }
    .metric-card h3 { margin: 15px 0 10px; color: #0077b6; }
    .metric-card .value { font-size: 2.7rem; font-weight: bold; color: #1a1a2e; }
    .metric-card .label { text-transform: uppercase; font-size: 0.9rem; color: #555555; }
    .pro-tip {
        background-color: #e8f4fd; padding: 15px; border-radius: 10px;
        display: flex; align-items: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.06); margin-top: 45px; color: #1a1a2e;
    }
    .pro-tip-icon { margin-right: 12px; font-size: 1.8rem; color: #0077b6; }
    .sidebar-arrow { animation: bounce 2s infinite; margin: 25px 0; color: #0077b6; font-size: 2rem; text-align: center; }
    .hr-divider { border: none; height: 1px; background: linear-gradient(90deg, #00a86b, #0077b6); margin: 20px 0; }
    footer { display: none; } header { display: none; }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-12px); }
        60% { transform: translateY(-6px); }
    }
</style>
"""

# ── Inject active theme CSS ────────────────────────────────────────────────────
st.markdown(DARK_CSS if is_dark else LIGHT_CSS, unsafe_allow_html=True)

# ── Theme toggle button (top-right) ───────────────────────────────────────────
_, btn_col = st.columns([9, 1])
with btn_col:
    st.button(
        "☀️ Light" if is_dark else "🌙 Dark",
        on_click=toggle_theme,
        use_container_width=True,
    )

# ── Latest metrics ─────────────────────────────────────────────────────────────
def get_latest_metrics(df):
    latest_data    = df.iloc[-1]
    calories       = latest_data.get("Calories_Burned", 0)
    steps          = latest_data.get("Steps", 0)
    water_intake   = latest_data.get("Water_Intake_Liters", 0)
    sleep          = latest_data.get("Sleep_Hours", 0)
    recovery_score = latest_data.get("Recovery_Score", 0)
    return calories, steps, water_intake, sleep, recovery_score

calories, steps, water_intake, sleep, recovery_score = get_latest_metrics(df)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="pill-badge">Premium Fitness Tracker</div>', unsafe_allow_html=True)
st.markdown('<h1 class="headline-gradient">Welcome to FitSync</h1>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;font-size:1.1rem;'>"
    "Your ultimate personal health analytics dashboard for tracking workouts, nutrition, sleep, and vitals."
    "</p>",
    unsafe_allow_html=True,
)
st.markdown('<div class="sidebar-arrow">⬇️ Open the sidebar to navigate</div>', unsafe_allow_html=True)
st.markdown('<hr class="hr-divider">', unsafe_allow_html=True)

# ── Today's Snapshot ───────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Calories Burned</div>
        <div class="value">{calories}</div>
        <div>🔥 Good job!</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Steps Today</div>
        <div class="value">{steps}</div>
        <div>🏃‍♂️ Keep it up!</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Hydration</div>
        <div class="value">{water_intake}L</div>
        <div>💧 Stay hydrated!</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Sleep Last Night</div>
        <div class="value">{sleep}h</div>
        <div>🛌 {recovery_score}% recovery</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="hr-divider">', unsafe_allow_html=True)

# ── Feature Grid ───────────────────────────────────────────────────────────────
fcols = st.columns(3)
features = [
    ("Workouts",        "Track your workouts, set goals, and measure progress.",  "🏋️‍♂️"),
    ("Nutrition",       "Log your meals and plan healthier dietary choices.",      "🥗"),
    ("Sleep Quality",   "Monitor your sleep patterns for better health.",          "🛌"),
    ("Vitals & Health", "Keep tabs on your health with vital signs.",              "❤️"),
    ("Progress Charts", "Visualize your progress with dynamic charts.",            "📈"),
    ("Goals & Streaks", "Set health goals and build streaks for motivation.",      "🎯"),
]

for i, (title, desc, icon) in enumerate(features):
    with fcols[i % 3]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">{title}</div>
            <div class="value">{icon}</div>
            <div>{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="hr-divider">', unsafe_allow_html=True)

# ── Pro Tip ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pro-tip">
    <div class="pro-tip-icon">💡</div>
    <div>Pro Tip: Connect your wearable devices to seamlessly integrate health data into FitSync.</div>
</div>
""", unsafe_allow_html=True)