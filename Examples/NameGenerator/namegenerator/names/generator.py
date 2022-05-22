import random
import string

from namegenerator.names.core import Name

_male_first_names = [
    "James",
    "Robert",
    "John",
    "David",
    "William",
    "Peter",
    "Michael",
    "Richard",
    "Thomas",
    "Charles",
    "Larry",
]

_female_first_names = [
    "Linda",
    "Mary",
    "Patricia",
    "Barbara",
    "Susan",
    "Sandra",
    "Maria",
    "Nancy",
    "Carol",
    "Sharon",
    "Jane"
]

_last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Miller",
    "Davis",
    "Garcia",
    "Rodriguez",
    "Wilson",
    "Martinez",
    "Anderson",
    "Taylor",
    "Thomas",
    "Hernandez",
    "Moore",
    "Martin",
    "Jackson",
    "Thompson",
    "White",
    "Lopez",
    "Doe"
]


def generate_name(female_name=True, add_middle_initial=False):
    first_name = random.choice(
        _female_first_names if female_name else _male_first_names)
    last_name = random.choice(_last_names)
    middle_initial = random.choice(
        string.ascii_uppercase) if add_middle_initial else ""
    return Name(first_name, last_name, middle_initial)
