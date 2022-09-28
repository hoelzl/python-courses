# %% tags=["del"]
from project import Project
from employee_v1 import (
    EmployeeDao,
    EmployeeType,
    EmployeeV1,
    HourReporter,
    PaymentCalculator,
    ReportPrinter,
)
from augurdb import AugurDatabase
from pprint import pprint


# %%
p1 = Project(name="Project 1", assets=10_000.0)
p2: Project = Project(name="Project 2", assets=12_000.0)

# %%
db = AugurDatabase()

# %%
default_payment_calculator = PaymentCalculator()
default_hour_reporter = HourReporter()
default_report_printer = ReportPrinter()
default_employee_dao = EmployeeDao(db)

# %%
e1 = EmployeeV1(
    id=123,
    name="Joe Random",
    salary=1000.0,
    overtime=5,
    employee_type=EmployeeType.REGULAR,
    project=p1,
    payment_calculator=default_payment_calculator,
    hour_reporter=default_hour_reporter,
    report_printer=default_report_printer,
    dao=default_employee_dao,
)

# %%
e2 = EmployeeV1(
    id=124,
    name="Jane Ransom",
    salary=1500.0,
    overtime=43,
    employee_type=EmployeeType.HOURED,
    project=p1,
    payment_calculator=default_payment_calculator,
    hour_reporter=default_hour_reporter,
    report_printer=default_report_printer,
    dao=default_employee_dao,
)

# %%
e3 = EmployeeV1(
    id=125,
    name="Jill Chance",
    salary=2500.0,
    overtime=2,
    employee_type=EmployeeType.COMMISSIONED,
    project=p2,
    payment_calculator=default_payment_calculator,
    hour_reporter=default_hour_reporter,
    report_printer=default_report_printer,
    dao=default_employee_dao,
)

# %%
employees = [e1, e2, e3]

# %%
for e in employees:
    print("=" * 35)
    print(f"{e.name} has a salary of {e.calculate_pay():.2f}")
    e.print_report()
    e.save_employee()
print("=" * 35)

# %%
pprint(db.records)
