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
tabs = [
    "Executive Overview",
    "Supplier Intelligence",
    "Project Tracking",
    "Operational Risk Insights",
    "Data Story"
]
selected_tab = st.sidebar.radio("Select a section", tabs)

# Executive Overview
if selected_tab == "Executive Overview":
    st.subheader("Executive Overview")

    total_projects = len(projects)
    active_projects = len(projects[projects["Status"] == "Active"])
    delayed_projects = len(projects[projects["Status"] == "Delayed"])
    avg_completion = round(projects["Completion_Percentage"].mean(), 1)
    total_budget = projects["Budget"].sum()
    total_actual_cost = projects["Actual_Cost"].sum()
    budget_variance = total_actual_cost - total_budget

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Projects", total_projects)
    col2.metric("Active Projects", active_projects)
    col3.metric("Delayed Projects", delayed_projects)
    col4.metric("Avg Completion", f"{avg_completion}%")

    col5, col6 = st.columns(2)

    col5.metric("Total Budget", f"£{total_budget:,.0f}")
    col6.metric("Budget Variance", f"£{budget_variance:,.0f}")

    st.subheader("Project Status Distribution")
    project_status_counts = projects["Status"].value_counts()
    fig = px.bar(
        x=project_status_counts.index,
        y=project_status_counts.values,
        labels={"x": "Project Status", "y": "Number of Projects"},
        title="Projects by Status"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Projects Requiring Attention")
    attention_projects = projects[
        (projects["Status"] == "Delayed") |
        (projects["Risk_Level"] == "High") |
        (projects["Delay_Days"] > 20)
    ]

    st.dataframe(attention_projects, use_container_width=True)


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
    fig = px.bar(suppliers, x="Supplier_Name", y="Quality_Score", color="Category", title="Supplier Quality Scores")
    st.plotly_chart(fig)
    
    st.subheader("Supplier On-Time Delivery Rates")
    fig = px.scatter(suppliers, x="Supplier_Name", y="Delivery_Reliability", color="Category", title="Supplier Delivery Reliability")
    st.plotly_chart(fig)
    
# Run this app locally using: streamlit run app.py
