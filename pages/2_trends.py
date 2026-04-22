import streamlit as st
from modules.processor import process_data
import plotly.express as px
import pandas as pd
from utils import apply_theme

# Use st.cache_data for caching
@st.cache_data
def load_data():
    return process_data()

# Configure the Streamlit page
st.set_page_config(layout="wide", page_title="Trends and Insights")

# Title of the page
st.title("Trends and Insights")

# Add a separator
st.markdown("---")

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

# Add a separator
st.markdown("---")

# Show summary statistics
st.subheader("Summary Statistics")
st.write(filtered_df[['Recovery_score', 'sleep_hours', 'steps', 'calories_burned']].describe().transpose())

# Add a separator
st.markdown("---")

# Line chart: Average Recovery Score Month Wise
st.subheader("Average Recovery Score by Month")
df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
monthly_avg_recovery = df.groupby('month')['Recovery_score'].mean().reset_index()
monthly_avg_recovery['month'] = monthly_avg_recovery['month'].astype(str)  # Convert Period to string
monthly_avg_recovery_fig = px.line(
    monthly_avg_recovery, 
    x='month', 
    y='Recovery_score', 
    labels={'month': 'Month', 'Recovery_score': 'Average Recovery Score'},
    title='Average Recovery Score by Month'
)
st.plotly_chart(monthly_avg_recovery_fig, use_container_width=True)

# Add a separator
st.markdown("---")

# Histograms: Distribution of Steps, Calories Burned, Recovery Score, Sleep Hours
st.subheader("Distribution of Metrics")
metrics = ['steps', 'calories_burned', 'Recovery_score', 'sleep_hours']
for metric in metrics:
    st.write(f"### Distribution of {metric.replace('_', ' ').title()}")
    histogram_fig = px.histogram(
        filtered_df, 
        x=metric, 
        title=f"Distribution of {metric.replace('_', ' ').title()}",
        nbins=30
    )
    st.plotly_chart(histogram_fig, use_container_width=True)
    st.markdown("---")  # Add a separator between histograms