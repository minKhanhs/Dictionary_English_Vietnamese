# Test FavoriteList - Kiểm tra quản lý danh sách từ yêu thích

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from models.FavoriteList import FavoriteList


class TestFavoriteList(unittest.TestCase):
    """Test Suite: Kiểm tra FavoriteList (danh sách từ yêu thích)"""

    def setUp(self):
        self.fav = FavoriteList()

    # --- Add ---

    def test_add_success(self):
        """Thêm từ yêu thích thành công"""
        result = self.fav.add("hello")
        self.assertTrue(result)
        self.assertEqual(self.fav.get_count(), 1)

    def test_add_normalizes_word(self):
        """Từ được normalize khi thêm"""
        self.fav.add("  HELLO  ")
        self.assertTrue(self.fav.contains("hello"))
        self.assertEqual(self.fav.get_item(0), "hello")

    def test_add_duplicate_rejected(self):
        """Không thêm từ trùng"""
        self.fav.add("hello")
        result = self.fav.add("hello")
        self.assertFalse(result)
        self.assertEqual(self.fav.get_count(), 1)

    def test_add_duplicate_case_insensitive(self):
        """Trùng kể cả khác hoa/thường"""
        self.fav.add("hello")
        result = self.fav.add("HELLO")
        self.assertFalse(result)
        self.assertEqual(self.fav.get_count(), 1)

    def test_add_empty_rejected(self):
        """Không thêm từ rỗng"""
        self.assertFalse(self.fav.add(""))
        self.assertFalse(self.fav.add(None))

    # --- Remove ---

    def test_remove_success(self):
        """Xóa từ yêu thích thành công"""
        self.fav.add("hello")
        result = self.fav.remove("hello")
        self.assertTrue(result)
        self.assertEqual(self.fav.get_count(), 0)

    def test_remove_not_found(self):
        """Xóa từ không tồn tại trả về False"""
        result = self.fav.remove("hello")
        self.assertFalse(result)

    def test_remove_case_insensitive(self):
        """Xóa không phân biệt hoa thường"""
        self.fav.add("hello")
        result = self.fav.remove("HELLO")
        self.assertTrue(result)
        self.assertEqual(self.fav.get_count(), 0)

    # --- Contains ---

    def test_contains_true(self):
        self.fav.add("hello")
        self.assertTrue(self.fav.contains("hello"))
        self.assertTrue(self.fav.contains("HELLO"))

    def test_contains_false(self):
        self.assertFalse(self.fav.contains("hello"))

    # --- Get item ---

    def test_get_item_valid(self):
        self.fav.add("hello")
        self.fav.add("world")
        self.assertEqual(self.fav.get_item(0), "hello")
        self.assertEqual(self.fav.get_item(1), "world")

    def test_get_item_out_of_bounds(self):
        """Lấy item ngoài phạm vi trả về None"""
        self.assertIsNone(self.fav.get_item(0))
        self.assertIsNone(self.fav.get_item(-1))

    # --- Clear ---

    def test_clear(self):
        """Xóa toàn bộ danh sách"""
        self.fav.add("hello")
        self.fav.add("world")
        self.fav.clear()
        self.assertEqual(self.fav.get_count(), 0)
        self.assertEqual(self.fav.to_list(), [])

    # --- to_list ---

    def test_to_list(self):
        """Trả về bản sao danh sách"""
        self.fav.add("a")
        self.fav.add("b")
        result = self.fav.to_list()
        self.assertEqual(result, ["a", "b"])
        # Bản sao
        result.append("c")
        self.assertEqual(self.fav.get_count(), 2)

    def test_to_list_empty(self):
        self.assertEqual(self.fav.to_list(), [])

    # --- Multiple operations ---

    def test_add_remove_add(self):
        """Thêm → xóa → thêm lại cùng từ được phép"""
        self.fav.add("hello")
        self.fav.remove("hello")
        result = self.fav.add("hello")
        self.assertTrue(result)
        self.assertEqual(self.fav.get_count(), 1)


if __name__ == "__main__":
    unittest.main()
