import printer
import names

print("Loading run.py")
print(f"__name__ is {__name__}")


def run_program():
    print("run.py started as main program.")
    printer.print_greeting(names.get_name())
    print(printer.my_fun())
    print(names.my_fun())


if __name__ == "__main__":
    run_program()
