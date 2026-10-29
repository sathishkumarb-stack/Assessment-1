
import csv
from pathlib import Path

DATA_FILE = Path("data/employees.csv")

EMPLOYEES = [
    {"id": 1, "name": "Arun", "department": "Sales", "salary": 30000, "city": "Chennai"},
    {"id": 2, "name": "Priya", "department": "HR", "salary": 45000, "city": "Chennai"},
    {"id": 3, "name": "Rahul", "department": "IT", "salary": 60000, "city": "Bangalore"},
    {"id": 4, "name": "Divya", "department": "IT", "salary": 75000, "city": "Chennai"},
    {"id": 5, "name": "Karthik", "department": "Finance", "salary": 90000, "city": "Mumbai"},
    {"id": 6, "name": "Meena", "department": "Sales", "salary": 52000, "city": "Bangalore"},
    {"id": 7, "name": "Suresh", "department": "IT", "salary": 68000, "city": "Chennai"},
    {"id": 8, "name": "Anitha", "department": "HR", "salary": 48000, "city": "Mumbai"},
]


def bonus(salary, rate=0.1, *extras, **options):
    """Calculate bonus and optionally apply a maximum cap."""
    result = salary * rate + sum(extras)
    if "cap" in options:
        result = min(result, options["cap"])
    return result


class InvalidSalaryError(ValueError):
    """Raised when an employee salary is negative."""


class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"{self.name} earns {self.salary}"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return f"{super().get_details()}, team size: {self.team_size}"


def main():
    above_50000 = [e["name"] for e in EMPLOYEES if e["salary"] > 50000]
    raised = list(map(lambda e: (e["name"], round(e["salary"] * 1.10, 2)), EMPLOYEES))
    chennai = list(filter(lambda e: e["city"] == "Chennai", EMPLOYEES))

    print("Bonus example:", bonus(50000, 0.1, 500, 250, cap=6000))
    print("Annual salary:", Employee("Arun", 30000).annual_salary())
    print("Manager:", Manager("Priya", 80000, 5).get_details())
    print("Above 50000:", above_50000)
    print("10% raise:", raised)
    print("Chennai:", [e["name"] for e in chennai])

    try:
        Employee("Invalid", -500)
    except InvalidSalaryError as error:
        print(f"Error: {error}")
    finally:
        print("Transaction finished")

    for employee in EMPLOYEES:
        salary = employee["salary"]
        if salary == 0:
            continue
        print(f'{employee["name"]}: {salary}')
        if salary > 85000:
            print("Stopping after first salary above 85000")
            break


if __name__ == "__main__":
    main()
