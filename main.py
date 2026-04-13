import streamlit as st
from modules.processor import process_data

# Configure the Streamlit page
st.set_page_config(layout="wide", page_title="FitSync")

# Title of the dashboard
st.title("FitSync - Personal Health Analytics")

# Add a separator
st.markdown("---")

# Load and process the data
with st.spinner('Loading and processing data...'):
    df = process_data()

# Show a preview of the data
# st.write("### Data Preview")
# st.dataframe(df.head(10))

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

# Placeholder for additional sections
# Add additional sections below, such as charts and insights
# For example:
# st.write("## Insights")
# st.bar_chart(df['Recovery_score'])