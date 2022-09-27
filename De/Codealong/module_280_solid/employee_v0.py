# %% tags=["keep"]
from augurdb import AugurDatabase

# %% tags=["del"]
from dataclasses import dataclass
from employee_type import EmployeeType
from project import Project


# %% tags=["keep"]
@dataclass
class EmployeeV0:
    id: int
    name: str
    salary: float
    overtime: int
    employee_type: EmployeeType
    project: Project
    database: AugurDatabase

    def calculate_pay(self) -> float:
        if self.employee_type == EmployeeType.REGULAR:
            return self.salary + 60.0 * self.overtime
        elif self.employee_type == EmployeeType.COMMISSIONED:
            return self.project.assets * 0.1
        elif self.employee_type == EmployeeType.HOURED:
            return 50.0 * self.overtime
        raise ValueError(f"{self.employee_type} is not valid.")

    def report_hours(self) -> int:
        if self.employee_type == EmployeeType.REGULAR:
            return 40 + self.overtime
        elif self.employee_type == EmployeeType.COMMISSIONED:
            # Commissioned employees always work 40 hours
            return 40
        elif self.employee_type == EmployeeType.HOURED:
            # We use overtime for the billed hours
            return self.overtime
        raise ValueError(f"{self.employee_type} is not valid.")

    def print_report(self) -> None:
        print(f"{self.name} worked {self.report_hours()} hours.")

    def save_employee(self) -> None:
        self.database.start_transaction()
        self.database.store_field(self.id, "name", self.name)
        self.database.store_field(self.id, "salary", self.salary)
        self.database.store_field(self.id, "overtime", self.overtime)
        self.database.store_field(self.id, "employee_type", self.employee_type)
        self.database.store_field(self.id, "project", self.project)
        self.database.commit_transaction()
