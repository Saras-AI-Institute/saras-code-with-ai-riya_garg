# utils.py
import streamlit as st
def apply_theme(theme: str):
    if theme == "Dark":
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #333;
                color: #fff;
            }
            .sidebar .sidebar-content {
                background-color: #444;
            }
            .stMetric {
                color: #fff !important;
            }
            .st-dataframe, .stTable {
                background-color: #000;
                border: 1px solid #fff;
                color: #fff;
            }
            .css-1d391kg p, .css-1d391kg, h1, h2, h3, h4, h5, h6, .css-145kmo2, .css-qbe2hs {
                color: #fff !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:  # Light theme
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #fff;
                color: #000;
            }
            .sidebar .sidebar-content {
                background-color: #f5f5f5;
            }
            .stMetric {
                color: #000 !important;
            }
            .st-dataframe, .stTable {
                background-color: #fff;
                border: 1px solid #000;
                color: #000;
            }
            .css-1d391kg p, .css-1d391kg, h1, h2, h3, h4, h5, h6, .css-145kmo2, .css-qbe2hs {
                color: #000 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )