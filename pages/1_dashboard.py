import plotly.express as px
import streamlit as st
from utils import apply_theme
from modules.processor import process_data

# Use st.cache_data for caching
@st.cache_data
def load_data():
    return process_data()

# Configure the Streamlit page
st.set_page_config(layout="wide", page_title="Dashboard")

# Title of the dashboard
st.title("FitSync - Personal Health Analytics")

st.markdown("## Dashboard")

# Improve visual appeal
st.markdown(
    """
    Welcome to the dashboard! Here is where you can track your health progress through various insights and metrics.
    - **Average Steps**: Stay motivated by tracking your steps.
    - **Average Sleep Hours**: Ensure you're getting enough rest.
    - **Recovery Score**: Monitor your recovery for optimal performance.
    """
)

# Theme selection
theme_option = st.sidebar.selectbox("Select Theme", ["Light", "Dark"], index=0)
apply_theme(theme_option)

# Load and process the data
with st.spinner('Loading and processing data...'):
    df = load_data()

# Add a sidebar for filters
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Filter the data based on the selected time range
if time_range == "Last 7 Days":
    filtered_df = df.sort_values(by='date', ascending=False).head(7)
elif time_range == "Last 30 Days":
    filtered_df = df.sort_values(by='date', ascending=False).head(30)
else:
    filtered_df = df

# Calculate metrics from the filtered dataframe
average_steps_filtered = filtered_df['steps'].mean()
average_sleep_hours_filtered = filtered_df['sleep_hours'].mean()
average_recovery_score_filtered = filtered_df['Recovery_score'].mean()

# Create a 3-column layout for the metrics
col1, col2, col3 = st.columns(3)

# Display metrics for the filtered data
col1.metric(label="Average Steps", value=f"{average_steps_filtered:.0f}", delta=None)
col2.metric(label="Average Sleep Hours", value=f"{average_sleep_hours_filtered:.1f}", delta=None)
col3.metric(label="Average Recovery Score", value=f"{average_recovery_score_filtered:.1f}", delta=None)
# Add a separator
st.markdown("---")

# Create two columns for dual line chart and scatter plot
chart_col1, chart_col2 = st.columns(2)

# Dual Line Chart: Recovery Score and Sleep Hours Over Time
with chart_col1:
    st.subheader("Recovery Score and Sleep Trend")
    recovery_sleep_fig = px.line(
        filtered_df,
        x='date',
        y=['Recovery_score', 'sleep_hours'],
        labels={'value': 'Score / Hours', 'date': 'Date'},
        title='Recovery Score and Sleep Trend'
    )
    st.plotly_chart(recovery_sleep_fig, use_container_width=True)

# Scatter Plot: Recovery Score vs Steps colored by Sleep Hours
with chart_col2:
    st.subheader("Recovery Score vs Daily Steps")
    scatter_fig = px.scatter(
        filtered_df,
        x='steps',
        y='Recovery_score',
        color='sleep_hours',
        labels={'steps': 'Steps', 'Recovery_score': 'Recovery Score'},
        title='Recovery Score vs Daily Steps'
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

# Add a separator
st.markdown("---")

# Create two columns for the second set of charts
chart_col3, chart_col4 = st.columns(2)

# Scatter Plot: Recovery Score vs Resting Heart Rate
with chart_col3:
    st.subheader("Recovery Score vs Resting Heart Rate")
    heart_rate_scatter_fig = px.scatter(
        filtered_df,
        x='heart_rate_bpm',
        y='Recovery_score',
        labels={'heart_rate_bpm': 'Heart Rate (BPM)', 'Recovery_score': 'Recovery Score'},
        title='Recovery Score vs Resting Heart Rate'
    )
    st.plotly_chart(heart_rate_scatter_fig, use_container_width=True)

# Line Chart: Daily Calories Burned Trend
with chart_col4:
    st.subheader("Daily Calories Burned Trend")
    calories_burned_fig = px.line(
        filtered_df,
        x='date',
        y='calories_burned',
        labels={'date': 'Date', 'calories_burned': 'Calories Burned'},
        title='Daily Calories Burned Trend'
    )
    st.plotly_chart(calories_burned_fig, use_container_width=True)

# Note: Ensure charts are aligned properly and the layout remains clean and professional.
# Placeholder for additional sections
# Add additional sections below, such as charts and insights
# For example:
# st.write("## Insights")
# st.bar_chart(df['Recovery_score'])