# %%
from project import Project
from employee_srp import (
    CommissionedEmployment,
    EmployeeDao,
    EmployeeSrp,
    HouredEmployment,
    RegularEmployment,
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
default_report_printer = ReportPrinter()
default_employee_dao = EmployeeDao(db)

# %%
e1 = EmployeeSrp(
    id=123,
    name="Joe Random",
    employment=RegularEmployment(
        salary=1000.0,
        overtime=5,
    ),
    report_printer=default_report_printer,
    dao=default_employee_dao,
)

# %%
e2 = EmployeeSrp(
    id=124,
    name="Jane Ransom",
    employment=HouredEmployment(billable_hours=43),
    report_printer=default_report_printer,
    dao=default_employee_dao,
)

# %%
e3 = EmployeeSrp(
    id=125,
    name="Jill Chance",
    employment=CommissionedEmployment(project=p2),
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

# %%
