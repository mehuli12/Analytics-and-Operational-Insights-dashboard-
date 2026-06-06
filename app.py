import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load Sample Data (Simulating KB Infrastructure Data)
@st.cache_data
def load_data():
    num_suppliers = 50
    suppliers = pd.DataFrame({
        'Supplier_ID': range(1, num_suppliers + 1),
        'Supplier_Name': [f'Supplier_{i}' for i in range(1, num_suppliers + 1)],
        'Category': np.random.choice(['Raw Materials', 'Machinery', 'Services', 'Technology'], num_suppliers),
        'Average_Cost': np.random.randint(5000, 50000, num_suppliers),
        'On_Time_Delivery_Rate': np.random.uniform(80, 99, num_suppliers),
        'Quality_Rating': np.random.uniform(3.5, 5, num_suppliers),
        'Contract_Compliance': np.random.uniform(85, 100, num_suppliers)
    })
    
    num_projects = 100
    projects = pd.DataFrame({
        'Project_ID': range(1, num_projects + 1),
        'Project_Name': [f'Project_{i}' for i in range(1, num_projects + 1)],
        'Status': np.random.choice(['Active', 'Completed', 'Delayed'], num_projects),
        'Budget': np.random.randint(100000, 2000000, num_projects),
        'Actual_Cost': np.random.randint(80000, 2200000, num_projects),
        'Completion_Percentage': np.random.randint(50, 100, num_projects),
        'Delay_Days': np.random.randint(0, 90, num_projects)
    })
    
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
