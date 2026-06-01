import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.Menu import Menu


def runApplication():
    menu = Menu()
    menu.run()


def runTests():
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="Test*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def main():
    print("===== TỪ ĐIỂN ANH - VIỆT =====")
    print("1. Chạy ứng dụng")
    print("2. Chạy unit test")
    choice = input("Chọn: ")
    if choice == "2":
        runTests()
    else:
        runApplication()


if __name__ == "__main__":
    main()
