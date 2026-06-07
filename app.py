import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load simulated infrastructure operations data

@st.cache_data
def load_data():
    suppliers = pd.read_csv("data/suppliers.csv")
    projects = pd.read_csv("data/projects.csv")
    issues = pd.read_csv("data/issues.csv")
    return suppliers, projects, issues
    
# Load Data
suppliers, projects, issues = load_data()

# Calculate overall supplier score
suppliers["Supplier_Score"] = (
    suppliers["Delivery_Reliability"] * 0.35 +
    suppliers["Cost_Consistency"] * 0.25 +
    suppliers["Quality_Score"] * 0.25 +
    suppliers["Responsiveness_Score"] * 0.15
).round(1)

# Link projects to their primary suppliers
projects = projects.merge(
    suppliers[
        [
            "Supplier_ID",
            "Supplier_Name",
            "Supplier_Score",
            "Risk_Category"
        ]
    ],
    left_on="Primary_Supplier_ID",
    right_on="Supplier_ID",
    how="left"
)

projects = projects.rename(columns={
    "Supplier_Name": "Primary_Supplier",
    "Supplier_Score": "Primary_Supplier_Score",
    "Risk_Category": "Primary_Supplier_Risk"
})

# Calculate project risk score

issue_counts = issues.groupby("Project_ID").size().reset_index(name="Open_Issues")

projects = projects.merge(
    issue_counts,
    on="Project_ID",
    how="left"
)

projects["Open_Issues"] = projects["Open_Issues"].fillna(0)

# Normalize individual risk drivers to a 0-100 scale
projects["Schedule_Risk"] = (projects["Delay_Days"] / 60 * 100).clip(0, 100)

projects["Issue_Risk"] = (projects["Open_Issues"] / 10 * 100).clip(0, 100)

projects["Completion_Risk"] = (100 - projects["Completion_Percentage"]).clip(0, 100)

projects["Budget_Variance_Percent"] = (
    (projects["Actual_Cost"] - projects["Budget"]) / projects["Budget"] * 100
).round(1)

projects["Cost_Risk"] = (projects["Budget_Variance_Percent"] / 30 * 100).clip(0, 100)

# Weighted project risk score
projects["Risk_Score"] = (
    projects["Schedule_Risk"] * 0.40 +
    projects["Issue_Risk"] * 0.30 +
    projects["Completion_Risk"] * 0.20 +
    projects["Cost_Risk"] * 0.10
).round(0)




# Streamlit Layout
st.title("Operational Intelligence Dashboard")

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


# Operational Risk Insights
elif selected_tab == "Operational Risk Insights":
    st.subheader("Operational Risk Insights")

    st.write(
        "This section identifies projects that need management attention by combining "
        "delay days, open issues, completion progress, and operational severity signals."
    )

    high_risk_projects = projects.sort_values(by="Risk_Score", ascending=False)

    st.subheader("Highest Risk Projects")
    st.dataframe(
        high_risk_projects[
            [
                "Project_ID",
                "Project_Name",
                "Status",
                "Completion_Percentage",
                "Delay_Days",
                "Open_Issues",
                "Risk_Score",
            ]
        ],
        use_container_width=True,
    )

    st.subheader("Risk Score by Project")
    fig = px.bar(
        high_risk_projects,
        x="Project_Name",
        y="Risk_Score",
        color="Status",
        title="Project Risk Score"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Issue Category Breakdown")
    issue_category_counts = issues["Issue_Category"].value_counts().reset_index()
    issue_category_counts.columns = ["Issue_Category", "Count"]

    fig = px.bar(
        issue_category_counts,
        x="Issue_Category",
        y="Count",
        title="Most Common Operational Issue Categories"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Open High Severity Issues")
    high_severity_issues = issues[
        (issues["Severity"] == "High") & (issues["Status"] == "Open")
    ].sort_values(by="Days_Open", ascending=False)

    st.dataframe(high_severity_issues, use_container_width=True)

    st.subheader("Operational Alerts")

    critical_projects = high_risk_projects[high_risk_projects["Risk_Score"] >= 70]

    if len(critical_projects) == 0:
        st.success("No critical project risks detected.")
    else:
        for _, row in critical_projects.iterrows():
            st.warning(
                f"{row['Project_Name']} requires attention. "
                f"Risk Score: {row['Risk_Score']:.0f}/100. "
                f"Delay: {row['Delay_Days']} days. "
                f"Open Issues: {int(row['Open_Issues'])}."
            )


    st.subheader("Root Cause Analysis")

    top_risk_projects = high_risk_projects.head(5)

    for _, project in top_risk_projects.iterrows():
        project_issues = issues[issues["Project_ID"] == project["Project_ID"]]

        root_causes = (
            project_issues["Issue_Category"]
            .value_counts()
            .head(3)
            .index
            .tolist()
        )

        if len(root_causes) == 0:
            root_causes = ["No major issue category recorded"]


        st.markdown(f"### {project['Project_Name']}")
        st.write(f"Risk Score: {project['Risk_Score']:.0f}/100")
        st.write("Primary Drivers:")
        for cause in root_causes:
            st.write(f"- {cause}")

        st.write("Recommended Actions:")

        action_map = {
            "Supplier Delay": "Review supplier performance and identify backup vendors.",
            "Budget Overrun": "Conduct budget review and approve corrective actions.",
            "Resource Constraint": "Reallocate resources or adjust project priorities.",
            "Equipment Failure": "Escalate maintenance and equipment replacement planning.",
            "Permit Delay": "Escalate approvals and engage relevant stakeholders.",
            "Quality Issue": "Perform quality audit and implement corrective measures."
        }

        recommended_actions = []

        for cause in root_causes:
            if cause in action_map:
                recommended_actions.append(action_map[cause])

        for action in recommended_actions:
            st.write(f"✓ {action}")

        st.divider()




# Data Story
elif selected_tab == "Data Story":

    st.title("Operational Intelligence Dashboard")

    st.header("Business Problem")

    st.write("""
    Operations teams often manage dozens of projects, suppliers, budgets,
    and operational issues simultaneously. As projects scale, it becomes
    increasingly difficult to identify which risks require immediate
    intervention and which suppliers are contributing to delivery delays.

    This dashboard was designed to provide a centralized view of project
    health, supplier performance, and operational risk so that decision
    makers can prioritize actions and allocate resources effectively.
    """)

    st.header("Dataset")

    st.write("""
    This project uses simulated infrastructure operations data inspired by
    real-world project management, supplier evaluation, procurement, and
    operational reporting scenarios.

    No confidential company data has been used.

    The dataset contains:

    • Projects
    • Suppliers
    • Operational Issues
    • Risk Indicators
    """)

    st.header("Supplier Scoring Methodology")

    st.write("""
    Suppliers are evaluated using four operational metrics:

    • Delivery Reliability
    • Cost Consistency
    • Quality Score
    • Responsiveness Score

    Overall Supplier Score =
    35% Delivery Reliability +
    25% Cost Consistency +
    25% Quality +
    15% Responsiveness

    Suppliers are then categorized as:

    • Recommended
    • Monitor
    • High Risk
    """)


    st.header("Project Risk Methodology")

    st.write("""
    Project Risk Score is calculated using a weighted operational risk model.
    
    The model combines four risk drivers:
    
    • Schedule Risk (40%)
    • Issue Risk (30%)
    • Completion Risk (20%)
    • Cost Risk (10%)
    
    Each risk driver is normalized to a 0–100 scale before weighting.
    
    Schedule Risk:
    Measures the impact of project delays.

    Issue Risk:
    Measures the impact of unresolved operational issues.
    
    Completion Risk:
    Measures delivery risk based on remaining work.
    
    Cost Risk:
    Measures budget overrun exposure.
    
    The final score is designed to prioritize management attention and
    highlight projects requiring intervention.
    
    This is a heuristic decision-support model rather than a predictive
    forecasting model.
    """)



    st.header("Decisions Supported")

    st.write("""
    This dashboard supports decisions such as:

    • Which projects require immediate attention?
    • Which suppliers should be reviewed?
    • Which operational issues are most common?
    • Where should management resources be focused?
    • What risks could impact delivery performance?
    """)

    st.header("Limitations")

    st.write("""
    This project uses simulated operational data and simplified scoring
    models for demonstration purposes.

    In a production environment, additional factors such as resource
    availability, procurement lead times, financial forecasts, and
    historical supplier performance would be incorporated into the model.
    """)



# Run this app locally using: streamlit run app.py
