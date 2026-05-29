# main.py - Điểm khởi động chương trình từ điển Anh-Việt

import sys
import os
import unittest

# Đảm bảo thư mục gốc trong sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.Menu import Menu


def run_application():
    """Khởi chạy ứng dụng từ điển."""
    menu = Menu()
    menu.run()


def run_tests():
    """Khởi chạy toàn bộ unit test."""
    # Tự động discover tất cả file Test*.py trong thư mục tests/
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
        run_tests()
    else:
        run_application()


if __name__ == "__main__":
    main()
