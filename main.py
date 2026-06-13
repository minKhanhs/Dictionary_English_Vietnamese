import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.ResponseCode import ResponseCode
from ui.Menu import Menu


def runApplication():
    try:
        menu = Menu()
        menu.run()
    except Exception as e:
        print(f"{ResponseCode.FAIL_LABEL} runApplication: {e}")


def runTests():
    try:
        loader = unittest.TestLoader()
        suite = loader.discover("tests", pattern="Test*.py")
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    except Exception as e:
        print(f"{ResponseCode.FAIL_LABEL} runTests: {e}")


def main():
    print("===== TỪ ĐIỂN ANH - VIỆT =====")
    print("1. Chạy ứng dụng")
        print("2. Chạy test suite")
    try:
        choice = input("Chọn: ")
        if choice == "2":
            runTests()
        else:
            runApplication()
    except KeyboardInterrupt:
        print(f"\n{ResponseCode.SKIP_LABEL} Đã dừng bởi người dùng.")
    except Exception as e:
        print(f"{ResponseCode.FAIL_LABEL} main: {e}")


if __name__ == "__main__":
    main()
