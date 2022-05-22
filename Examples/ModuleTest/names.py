print("Loading names.py")
print(f"__name__ is {__name__}")


def get_name():
    return "Hans"


def my_fun():
    return "names.my_fun()"


if __name__ == "__main__":
    print("names.py started as main program.")
