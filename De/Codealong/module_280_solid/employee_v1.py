# %% tags=["del"]
from dataclasses import dataclass
from augurdb import AugurDatabase
from employee_type import EmployeeType
from project import Project

# %%
class PaymentCalculator:
    def calculate_pay(self, employee: "EmployeeV1") -> float:
        employee_type = employee.employee_type
        if employee_type == EmployeeType.REGULAR:
            return employee.salary + 60.0 * employee.overtime
        elif employee_type == EmployeeType.COMMISSIONED:
            return employee.project.assets * 0.1
        elif employee_type == EmployeeType.HOURED:
            return 50.0 * employee.overtime
        raise ValueError(f"{employee_type} is not valid.")


# %%
class HourReporter:
    def report_hours(self, employee: "EmployeeV1") -> int:
        employee_type = employee.employee_type
        if employee_type == EmployeeType.REGULAR:
            return 40 + employee.overtime
        elif employee_type == EmployeeType.COMMISSIONED:
            # Commissioned employees always work 40 hours
            return 40
        elif employee_type == EmployeeType.HOURED:
            # We use overtime for the billed hours
            return employee.overtime
        raise ValueError(f"{employee_type} is not valid.")

# %%
class ReportPrinter:
    def print_report(self, employee: "EmployeeV1") -> None:
        print(f"{employee.name} worked {employee.report_hours()} hours.")

# %%
@dataclass
class EmployeeDao:
    database: AugurDatabase

    def save_employee(self, employee: "EmployeeV1") -> None:
        self.database.start_transaction()
        self.database.store_field(employee.id, "name", employee.name)
        self.database.store_field(employee.id, "salary", employee.salary)
        self.database.store_field(employee.id, "overtime", employee.overtime)
        self.database.store_field(employee.id, "employee_type", employee.employee_type)
        self.database.store_field(employee.id, "project", employee.project)
        self.database.commit_transaction()

# %%
@dataclass
class EmployeeV1:
    id: int
    name: str
    salary: float
    overtime: int
    employee_type: EmployeeType
    project: Project
    payment_calculator: PaymentCalculator
    hour_reporter: HourReporter
    report_printer: ReportPrinter
    dao: EmployeeDao

    def calculate_pay(self):
        return self.payment_calculator.calculate_pay(self)

    def report_hours(self):
        return self.hour_reporter.report_hours(self)

    def print_report(self):
        return self.report_printer.print_report(self)

    def save_employee(self):
        return self.dao.save_employee(self)
