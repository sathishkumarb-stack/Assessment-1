# """Task 2: CSV/JSON files, REST API, and environment variables."""
import csv
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
CSV_PATH = DATA / "employees.csv"


def ensure_employee_csv():
    if CSV_PATH.exists():
        return
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
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "department", "salary", "city"])
        writer.writerows(rows)


def main():
    ensure_employee_csv()
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        employees = list(csv.DictReader(f))

    for employee in employees:
        employee["id"] = int(employee["id"])
        employee["salary"] = float(employee["salary"])

    (DATA / "employees.json").write_text(
        json.dumps(employees, indent=2), encoding="utf-8"
    )
    high_earners = [e for e in employees if e["salary"] > 50000]
    with (DATA / "high_earners.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "department", "salary", "city"])
        writer.writeheader()
        writer.writerows(high_earners)

    print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")

    load_dotenv(ROOT / ".env")
    print("API_KEY loaded:", "yes" if os.getenv("API_KEY") else "no (optional for this API)")

    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=5)
        response.raise_for_status()
        users = response.json()
        for user in users[:3]:
            print(f'{user.get("id")} - {user.get("name")} - {user.get("email")}')

        parsed = [{
            "id": u.get("id"),
            "name": u.get("name"),
            "email": u.get("email"),
            "city": u.get("address", {}).get("city"),
            "company": u.get("company", {}).get("name"),
        } for u in users]
        (DATA / "users.json").write_text(json.dumps(parsed, indent=2), encoding="utf-8")

        missing = requests.get(
            "https://jsonplaceholder.typicode.com/users/9999", timeout=5
        )
        if missing.status_code == 404:
            print("/users/9999 -> 404 Not found")
        else:
            print(f"/users/9999 -> HTTP {missing.status_code}")
    except requests.exceptions.Timeout:
        print("API request timed out (timeout=5).")
    except requests.exceptions.ConnectionError:
        print("API connection failed; check your internet connection.")
    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")


if __name__ == "__main__":
    main()
