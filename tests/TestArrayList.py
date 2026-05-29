# Test ArrayList - Kiểm tra cấu trúc mảng động

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from structures.ArrayList import ArrayList


class TestArrayList(unittest.TestCase):
    """Test Suite: Kiểm tra ArrayList (mảng động tự cài đặt)"""

    def setUp(self):
        self.arr = ArrayList()

    # --- Add & Get ---

    def test_add_and_get(self):
        """Thêm phần tử và lấy ra"""
        self.arr.add("hello")
        self.arr.add("world")
        self.assertEqual(self.arr.get(0), "hello")
        self.assertEqual(self.arr.get(1), "world")

    def test_add_multiple_elements(self):
        """Thêm nhiều phần tử vượt capacity ban đầu (10)"""
        for i in range(15):
            self.arr.add(i)
        self.assertEqual(self.arr.size(), 15)
        self.assertEqual(self.arr.get(14), 14)

    def test_get_out_of_bounds(self):
        """Lấy phần tử ngoài phạm vi phải raise IndexError"""
        with self.assertRaises(IndexError):
            self.arr.get(0)
        self.arr.add("x")
        with self.assertRaises(IndexError):
            self.arr.get(1)

    # --- Size ---

    def test_size_empty(self):
        """Mảng rỗng có size = 0"""
        self.assertEqual(self.arr.size(), 0)

    def test_size_after_add(self):
        self.arr.add("a")
        self.arr.add("b")
        self.assertEqual(self.arr.size(), 2)

    # --- Remove ---

    def test_remove_middle(self):
        """Xóa phần tử ở giữa, các phần tử phía sau dời lên"""
        self.arr.add("a")
        self.arr.add("b")
        self.arr.add("c")
        self.arr.remove(1)
        self.assertEqual(self.arr.size(), 2)
        self.assertEqual(self.arr.get(0), "a")
        self.assertEqual(self.arr.get(1), "c")

    def test_remove_last(self):
        """Xóa phần tử cuối"""
        self.arr.add("a")
        self.arr.add("b")
        self.arr.remove(1)
        self.assertEqual(self.arr.size(), 1)
        self.assertEqual(self.arr.get(0), "a")

    def test_remove_out_of_bounds(self):
        """Xóa ngoài phạm vi phải raise IndexError"""
        with self.assertRaises(IndexError):
            self.arr.remove(0)

    # --- Contains ---

    def test_contains_true(self):
        self.arr.add("hello")
        self.arr.add("world")
        self.assertTrue(self.arr.contains("hello"))
        self.assertTrue(self.arr.contains("world"))

    def test_contains_false(self):
        self.arr.add("hello")
        self.assertFalse(self.arr.contains("world"))

    def test_contains_empty(self):
        self.assertFalse(self.arr.contains("anything"))

    # --- toString ---

    def test_to_string(self):
        self.arr.add("a")
        self.arr.add("b")
        result = self.arr.toString()
        self.assertIn("a", result)
        self.assertIn("b", result)

    # --- Edge cases ---

    def test_add_none(self):
        """Thêm None không crash"""
        self.arr.add(None)
        self.assertIsNone(self.arr.get(0))
        self.assertEqual(self.arr.size(), 1)

    def test_resize_happens(self):
        """Thêm > 10 phần tử (capacity ban đầu) → resize tự động"""
        for i in range(20):
            self.arr.add(i)
        self.assertEqual(self.arr.size(), 20)
        # Tất cả giá trị vẫn đúng sau resize
        for i in range(20):
            self.assertEqual(self.arr.get(i), i)


if __name__ == "__main__":
    unittest.main()
