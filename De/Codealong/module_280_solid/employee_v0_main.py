# %% tags=["del"]
from project import Project
from employee_v0 import EmployeeType, EmployeeV0
from augurdb import AugurDatabase

# %% tags=["keep"]
from pprint import pprint

# %% tags=["keep"]
p1 = Project(name="Project 1", assets=10_000.0)
p2: Project = Project(name="Project 2", assets=12_000.0)

# %% tags=["keep"]
db = AugurDatabase()

# %% tags=["keep"]
e1 = EmployeeV0(
    id=123,
    name="Joe Random",
    salary=1000.0,
    overtime=5,
    employee_type=EmployeeType.REGULAR,
    project=p1,
    database=db,
)

# %% tags=["keep"]
e2 = EmployeeV0(
    id=124,
    name="Jane Ransom",
    salary=1500.0,
    overtime=43,
    employee_type=EmployeeType.HOURED,
    project=p1,
    database=db,
)

# %% tags=["keep"]
e3 = EmployeeV0(
    id=125,
    name="Jill Chance",
    salary=2500.0,
    overtime=2,
    employee_type=EmployeeType.COMMISSIONED,
    project=p2,
    database=db,
)

# %% tags=["keep"]
employees = [e1, e2, e3]

# %% tags=["keep"]
for e in employees:
    print("=" * 35)
    print(f"{e.name} has a salary of {e.calculate_pay():.2f}")
    e.print_report()
    e.save_employee()
print("=" * 35)

# %%
pprint(db.records)
