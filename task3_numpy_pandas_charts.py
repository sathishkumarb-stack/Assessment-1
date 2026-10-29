# """Task 3: NumPy, Pandas, data cleaning, joins, and charts."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
DATA.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)


def ensure_employee_csv():
    path = DATA / "employees.csv"
    if not path.exists():
        rows = [
            [1, "Arun", "Sales", 30000, "Chennai"],
            [2, "Priya", "HR", 45000, "Chennai"],
            [3, "Rahul", "IT", 60000, "Bangalore"],
            [4, "Divya", "IT", 75000, "Chennai"],
            [5, "Karthik", "Finance", 90000, "Mumbai"],
            [6, "Meena", "Sales", 52000, "Bangalore"],
            [7, "Suresh", "IT", 68000, "Chennai"],
            [8, "Anitha", "HR", 48000, "Mumbai"],
        ]
        pd.DataFrame(rows, columns=["id", "name", "department", "salary", "city"]).to_csv(path, index=False)
    return path


def main():
    marks = np.array([[78, 85, 90], [88, 76, 92], [67, 73, 80], [95, 91, 89]])
    print("Shape:", marks.shape)
    print("Student averages:", marks.mean(axis=1).round(2))
    print("Subject averages:", marks.mean(axis=0).round(2))
    print("Grace marks:\n", marks + 5)
    print("Weighted scores:", np.dot(marks, np.array([0.3, 0.3, 0.4])).round(2))

    df = pd.read_csv(ensure_employee_csv())
    print("\nDataFrame info:")
    df.info()
    print("\nDescribe:\n", df.describe(include="all"))
    print("\nloc:\n", df.loc[0:2, ["name", "salary"]])
    print("\niloc:\n", df.iloc[:3, :3])
    print("\nFiltered salary > 50000:\n", df[df["salary"] > 50000])

    # Add two missing salaries and a duplicate row, then clean the data.
    dirty = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    dirty.loc[1, "salary"] = np.nan
    dirty.loc[4, "salary"] = np.nan
    dirty["salary"] = pd.to_numeric(dirty["salary"], errors="coerce")
    median = dirty["salary"].median()
    dirty["salary"] = dirty["salary"].fillna(median)
    dirty = dirty.drop_duplicates().reset_index(drop=True)
    dirty["id"] = dirty["id"].astype(int)
    dirty["salary"] = dirty["salary"].astype(float)
    dirty.to_csv(DATA / "employees_cleaned.csv", index=False)
    print(f"Median used for missing salaries: {median}; cleaned rows: {len(dirty)}")

    departments = pd.DataFrame([
        ["Sales", "Ravi", 500000], ["HR", "Lakshmi", 300000],
        ["IT", "Mohan", 900000], ["Finance", "Geetha", 400000],
        ["Marketing", "Kumar", 350000],
    ], columns=["department", "head", "budget"])
    departments.to_csv(DATA / "departments.csv", index=False)

    stats = dirty.groupby("department").agg(
        headcount=("id", "count"),
        average_salary=("salary", "mean"),
        maximum_salary=("salary", "max"),
    ).reset_index()
    stats.to_csv(REPORTS / "department_stats.csv", index=False)
    print("\nDepartment summary:\n", stats.round(2).to_string(index=False))

    for join_type in ("inner", "left", "outer"):
        dirty.merge(departments, on="department", how=join_type).to_csv(
            REPORTS / f"merge_{join_type}.csv", index=False
        )
    print("Departments with no employees:",
          sorted(set(departments.department) - set(dirty.department)))

    avg_salary = df.groupby("department")["salary"].mean().sort_values()
    fig, ax = plt.subplots()
    avg_salary.plot(kind="bar", ax=ax, label="Average salary")
    ax.set(title="Average Salary by Department", xlabel="Department", ylabel="Salary")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "bar_department_salary.png")
    plt.close(fig)
    print("Insight (bar): IT has the highest average salary in the original data.")

    fig, ax = plt.subplots()
    df["salary"].plot(kind="hist", bins=5, ax=ax, label="Employee salary")
    ax.set(title="Employee Salary Distribution", xlabel="Salary", ylabel="Employees")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "histogram_salary.png")
    plt.close(fig)
    print("Insight (histogram): Salaries are spread across several salary bands.")

    fig, ax = plt.subplots()
    ax.scatter(df["id"], df["salary"], label="Employees")
    ax.set(title="Employee ID vs Salary", xlabel="Employee ID", ylabel="Salary")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "scatter_id_salary.png")
    plt.close(fig)
    print("Insight (scatter): Employee ID does not indicate a clear salary trend.")

    fig, ax = plt.subplots()
    df.sort_values("id").plot(x="id", y="salary", kind="line", marker="o", ax=ax, label="Salary")
    ax.set(title="Salary by Employee ID", xlabel="Employee ID", ylabel="Salary")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "line_salary_by_id.png")
    plt.close(fig)
    print("Insight (line): Salaries fluctuate rather than increasing consistently by ID.")


if __name__ == "__main__":
    main()
