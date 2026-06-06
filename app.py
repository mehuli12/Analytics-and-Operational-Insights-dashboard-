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

# Calculate overall supplier score
suppliers["Supplier_Score"] = (
    suppliers["Delivery_Reliability"] * 0.35 +
    suppliers["Cost_Consistency"] * 0.25 +
    suppliers["Quality_Score"] * 0.25 +
    suppliers["Responsiveness_Score"] * 0.15
).round(1)

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

# Supplier Intelligence
elif selected_tab == "Supplier Intelligence":
    st.subheader("Supplier Intelligence")

    st.write(
        "This section ranks suppliers using delivery reliability, cost consistency, "
        "quality score, and responsiveness. The goal is to identify which suppliers "
        "are reliable, which need monitoring, and which create operational risk."
    )

    supplier_summary = suppliers[
        [
            "Supplier_Name",
            "Category",
            "Delivery_Reliability",
            "Cost_Consistency",
            "Quality_Score",
            "Responsiveness_Score",
            "Supplier_Score",
            "Risk_Category",
        ]
    ].sort_values(by="Supplier_Score", ascending=False)

    st.subheader("Supplier Ranking")
    st.dataframe(supplier_summary, use_container_width=True)

    st.subheader("Top Suppliers by Overall Score")
    fig = px.bar(
        supplier_summary,
        x="Supplier_Name",
        y="Supplier_Score",
        color="Risk_Category",
        title="Overall Supplier Score"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Suppliers Requiring Attention")
    risky_suppliers = supplier_summary[
        supplier_summary["Risk_Category"].isin(["Monitor", "High Risk"])
    ]

    st.dataframe(risky_suppliers, use_container_width=True)
    
# Run this app locally using: streamlit run app.py
