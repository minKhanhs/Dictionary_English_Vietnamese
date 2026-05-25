from tests.all_tests import AllTests
from ui.menu import Menu


def run_application():
    menu = Menu()
    menu.run()


def main():
    print("1. Run application")
    print("2. Run unit tests")
    choice = input("Choose an option: ")
    if choice == "2":
        AllTests.run_all()
    else:
        run_application()


if __name__ == "__main__":
    main()
