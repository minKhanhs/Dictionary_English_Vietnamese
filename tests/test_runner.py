class TestRunner:
    """Tiny test runner used instead of external test libraries."""

    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def assert_true(self, condition, test_name):
        self.total_tests += 1
        if condition:
            self.passed_tests += 1
            print("[PASS]", test_name)
        else:
            self.failed_tests += 1
            print("[FAIL]", test_name)

    def assert_false(self, condition, test_name):
        self.assert_true(not condition, test_name)

    def assert_equal(self, expected, actual, test_name):
        self.total_tests += 1
        if expected == actual:
            self.passed_tests += 1
            print("[PASS]", test_name)
        else:
            self.failed_tests += 1
            print(f"[FAIL] {test_name}: expected {expected!r}, got {actual!r}")

    def print_summary(self):
        print("\nTest summary")
        print("Total:", self.total_tests)
        print("Passed:", self.passed_tests)
        print("Failed:", self.failed_tests)
        return self.failed_tests == 0
