# Test HistoryList - Kiểm tra quản lý lịch sử tra cứu

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.AppConfig import AppConfig
from models.HistoryList import HistoryList


class TestHistoryList(unittest.TestCase):
    """Test Suite: Kiểm tra HistoryList (lịch sử tra cứu gần đây)"""

    def setUp(self):
        self.history = HistoryList()

    # --- Add & Get ---

    def test_add_and_get(self):
        """Thêm và lấy item"""
        self.history.add("hello")
        self.history.add("world")
        self.assertEqual(self.history.get_item(0), "hello")
        self.assertEqual(self.history.get_item(1), "world")
        self.assertEqual(self.history.get_count(), 2)

    def test_add_normalizes_word(self):
        """Từ được normalize khi thêm"""
        self.history.add("  HELLO  ")
        self.assertEqual(self.history.get_item(0), "hello")

    def test_add_empty_rejected(self):
        """Không thêm từ rỗng"""
        result = self.history.add("")
        self.assertFalse(result)
        self.assertEqual(self.history.get_count(), 0)

    def test_add_none_rejected(self):
        """Không thêm None"""
        result = self.history.add(None)
        self.assertFalse(result)

    # --- FIFO eviction ---

    def test_max_size_eviction(self):
        """Khi vượt MAX_HISTORY_SIZE, phần tử cũ nhất bị xóa (FIFO)"""
        for i in range(AppConfig.MAX_HISTORY_SIZE + 5):
            self.history.add(f"word{i}")
        # count phải bằng MAX_HISTORY_SIZE
        self.assertEqual(self.history.get_count(), AppConfig.MAX_HISTORY_SIZE)
        # Phần tử cũ nhất (word0) đã bị xóa, phần tử đầu tiên giờ là word5
        self.assertEqual(self.history.get_item(0), "word5")

    def test_max_size_exact(self):
        """Thêm đúng MAX_HISTORY_SIZE phần tử, không bị xóa"""
        for i in range(AppConfig.MAX_HISTORY_SIZE):
            self.history.add(f"word{i}")
        self.assertEqual(self.history.get_count(), AppConfig.MAX_HISTORY_SIZE)
        self.assertEqual(self.history.get_item(0), "word0")

    # --- Get item ---

    def test_get_item_out_of_bounds(self):
        """Lấy item ngoài phạm vi trả về None"""
        self.assertIsNone(self.history.get_item(0))
        self.assertIsNone(self.history.get_item(-1))

    # --- Clear ---

    def test_clear(self):
        """Xóa toàn bộ lịch sử"""
        self.history.add("hello")
        self.history.add("world")
        self.history.clear()
        self.assertEqual(self.history.get_count(), 0)
        self.assertEqual(self.history.to_list(), [])

    # --- to_list ---

    def test_to_list(self):
        """Trả về bản sao danh sách"""
        self.history.add("a")
        self.history.add("b")
        result = self.history.to_list()
        self.assertEqual(result, ["a", "b"])
        # Bản sao - thay đổi list không ảnh hưởng history
        result.append("c")
        self.assertEqual(self.history.get_count(), 2)

    def test_to_list_empty(self):
        """Danh sách rỗng trả về []"""
        self.assertEqual(self.history.to_list(), [])


if __name__ == "__main__":
    unittest.main()
