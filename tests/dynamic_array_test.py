from structures.dynamic_array import DynamicArray


class DynamicArrayTest:
    @staticmethod
    def run(runner):
        array = DynamicArray(1)
        runner.assert_true(array.is_empty(), "array starts empty")
        array.push_back("a")
        array.push_back("b")
        runner.assert_equal(2, array.get_size(), "array grows size")
        runner.assert_true(array.capacity >= 2, "array resizes capacity")
        runner.assert_equal("a", array.get(0), "array get works")
        array.set(1, "c")
        runner.assert_equal("c", array.get(1), "array set works")
        runner.assert_equal("a", array.remove_at(0), "array remove returns item")
        runner.assert_equal(["c"], array.to_list(), "array shifts after remove")
        array.clear()
        runner.assert_true(array.is_empty(), "array clears")
