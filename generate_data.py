import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

project_names = [
    "Riverside Tower", "Greenfield Residences", "Metro Commercial Hub",
    "Lakeside Apartments", "City Business Park", "West End Plaza",
    "Innovation Centre", "Central Heights", "Parkview Residency",
    "Harbour Point", "Northgate Offices", "Southbank Retail Park",
    "Kingston Heights", "Urban Logistics Hub", "Canary Works",
    "Victoria Point", "Camden Square", "Horizon Estate",
    "Regent Commercial Centre", "Oakwood Residences"
]

supplier_names = [
    "Alpha Steel", "BuildTech Systems", "Prime Concrete", "Urban Machinery",
    "Skyline Services", "Metro Equipments", "Vertex Solutions",
    "Elite Contractors", "Foundation Supply", "Titan Infrastructure",
    "Rapid Build Co", "Core Materials", "Apex Engineering",
    "BlueLine Logistics", "Nova Electrical", "Summit Tools",
    "Pioneer Concrete", "NextGen Systems", "Atlas Machinery",
    "Sterling Services"
]

categories = ["Raw Materials", "Machinery", "Services", "Technology"]
issue_categories = [
    "Supplier Delay", "Budget Overrun", "Resource Constraint",
    "Equipment Failure", "Permit Delay", "Quality Issue"
]

# Suppliers
suppliers = []
for i in range(1, 31):
    delivery = np.random.randint(60, 99)
    cost = np.random.randint(65, 98)
    quality = np.random.randint(65, 99)
    responsiveness = np.random.randint(60, 99)

    score = round(
        delivery * 0.35 +
        cost * 0.25 +
        quality * 0.25 +
        responsiveness * 0.15,
        1
    )

    if score >= 85:
        risk = "Recommended"
    elif score >= 75:
        risk = "Monitor"
    else:
        risk = "High Risk"

    suppliers.append([
        i,
        f"{random.choice(supplier_names)} {i}",
        random.choice(categories),
        delivery,
        cost,
        quality,
        responsiveness,
        risk
    ])

suppliers_df = pd.DataFrame(suppliers, columns=[
    "Supplier_ID", "Supplier_Name", "Category",
    "Delivery_Reliability", "Cost_Consistency",
    "Quality_Score", "Responsiveness_Score", "Risk_Category"
])

# Projects
projects = []
for i in range(1, 51):
    status = random.choices(
        ["Active", "Completed", "Delayed"],
        weights=[0.45, 0.30, 0.25]
    )[0]

    budget = np.random.randint(500000, 3500000)

    if status == "Delayed":
        actual_cost = int(budget * np.random.uniform(1.05, 1.35))
        delay_days = np.random.randint(15, 90)
        completion = np.random.randint(40, 85)
        risk = "High"
    elif status == "Active":
        actual_cost = int(budget * np.random.uniform(0.85, 1.15))
        delay_days = np.random.randint(0, 25)
        completion = np.random.randint(45, 95)
        risk = random.choice(["Low", "Medium"])
    else:
        actual_cost = int(budget * np.random.uniform(0.85, 1.05))
        delay_days = np.random.randint(0, 8)
        completion = 100
        risk = "Low"


    primary_supplier_id = np.random.randint(1, 31)

    projects.append([
        i,
        f"{random.choice(project_names)} {i}",
        status,
        budget,
        actual_cost,
        completion,
        delay_days,
        risk,
        primary_supplier_id
    ])

projects_df = pd.DataFrame(projects, columns=[
    "Project_ID", "Project_Name", "Status", "Budget",
    "Actual_Cost", "Completion_Percentage", "Delay_Days",
    "Risk_Level", "Primary_Supplier_ID"
])

# Issues
issues = []
for i in range(1, 151):
    project_id = np.random.randint(1, 51)
    category = random.choice(issue_categories)
    severity = random.choices(
        ["Low", "Medium", "High"],
        weights=[0.25, 0.45, 0.30]
    )[0]
    days_open = np.random.randint(1, 60)
    status = random.choices(
        ["Open", "Closed"],
        weights=[0.70, 0.30]
    )[0]

    issues.append([
        i,
        project_id,
        category,
        severity,
        days_open,
        status
    ])

issues_df = pd.DataFrame(issues, columns=[
    "Issue_ID", "Project_ID", "Issue_Category",
    "Severity", "Days_Open", "Status"
])

suppliers_df.to_csv("data/suppliers.csv", index=False)
projects_df.to_csv("data/projects.csv", index=False)
issues_df.to_csv("data/issues.csv", index=False)

print("Data generated successfully.")
print("Created:")
print("- data/suppliers.csv")
print("- data/projects.csv")
print("- data/issues.csv")
