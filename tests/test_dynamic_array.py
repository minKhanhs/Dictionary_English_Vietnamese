import unittest

from structures.dynamic_array import DynamicArray


class DynamicArrayTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra DynamicArray tự cài đặt
    """
    def test_array_starts_empty(self):
        # Mảng mới tạo chưa có phần tử nào
        self.assertTrue(DynamicArray(1).is_empty())

    def test_array_grows_size_and_capacity(self):
        # Khi thêm quá capacity ban đầu, mảng phải tự tăng capacity
        array = DynamicArray(1)

        array.push_back("a")
        array.push_back("b")

        self.assertEqual(2, array.get_size())
        self.assertGreaterEqual(array.capacity, 2)

    def test_array_get_and_set_work(self):
        # get lấy đúng phần tử, set cập nhật đúng vị trí
        array = DynamicArray(1)
        array.push_back("a")
        array.push_back("b")

        self.assertEqual("a", array.get(0))
        array.set(1, "c")
        self.assertEqual("c", array.get(1))

    def test_remove_at_returns_item_and_shifts_array(self):
        # remove_at phải trả về phần tử bị xóa và dồn các phần tử phía sau lên
        array = DynamicArray(1)
        array.push_back("a")
        array.push_back("c")

        self.assertEqual("a", array.remove_at(0))
        self.assertEqual(["c"], array.to_list())

    def test_array_clears(self):
        # clear phải xóa toàn bộ phần tử
        array = DynamicArray(1)
        array.push_back("a")

        array.clear()

        self.assertTrue(array.is_empty())
