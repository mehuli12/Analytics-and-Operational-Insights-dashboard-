import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load simulated infrastructure operations data
@st.cache_data
def load_data():
    suppliers = pd.read_csv("data/suppliers.csv")
    projects = pd.read_csv("data/projects.csv")
    return suppliers, projects
    
# Load Data
suppliers, projects = load_data()

# Streamlit Layout
st.title("Analytics and Operational Insights Dashboard")

# Tabs for Different Sections
st.sidebar.title("Navigation")
tabs = ["Financial Performance", "Project Tracking", "Supplier Performance"]
selected_tab = st.sidebar.radio("Select a section", tabs)

# Financial Performance
if selected_tab == "Financial Performance":
    st.subheader("Revenue & Expenses Overview")
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    financials = pd.DataFrame({
        'Month': months,
        'Revenue': np.random.randint(500000, 5000000, 12),
        'Expenses': np.random.randint(200000, 3000000, 12),
        'Profit': np.random.randint(100000, 2000000, 12)
    })
    fig = px.line(financials, x='Month', y=['Revenue', 'Expenses', 'Profit'], title="Financial Performance Over Time")
    st.plotly_chart(fig)

# Project Tracking
elif selected_tab == "Project Tracking":
    st.subheader("Project Status Overview")
    project_status_counts = projects["Status"].value_counts()
    fig = px.pie(values=project_status_counts, names=project_status_counts.index, title="Project Status Distribution")
    st.plotly_chart(fig)

    st.subheader("Budget vs Actual Cost")
    fig = px.scatter(projects, x="Budget", y="Actual_Cost", color="Status", title="Budget vs Actual Cost")
    st.plotly_chart(fig)

# Supplier Performance
elif selected_tab == "Supplier Performance":
    st.subheader("Supplier Quality Ratings")
    fig = px.bar(suppliers, x="Supplier_Name", y="Quality_Rating", color="Category", title="Supplier Quality Ratings")
    st.plotly_chart(fig)
    
    st.subheader("Supplier On-Time Delivery Rates")
    fig = px.scatter(suppliers, x="Supplier_Name", y="On_Time_Delivery_Rate", color="Category", title="Supplier On-Time Delivery Rates")
    st.plotly_chart(fig)

# Run this script using: streamlit run your_script.py
