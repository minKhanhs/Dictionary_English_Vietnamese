import os
import unittest


class AllTests:
    @staticmethod
    def run_all():
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        suite = unittest.defaultTestLoader.discover(tests_dir, pattern="test_*.py")
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        return result.wasSuccessful()


if __name__ == "__main__":
    AllTests.run_all()
