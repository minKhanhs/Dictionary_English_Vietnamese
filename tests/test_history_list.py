import unittest

from config.app_config import AppConfig
from models.history_list import HistoryList


class HistoryListTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra danh sách lịch sử tra cứu
    """
    def test_history_starts_empty(self):
        # History mới tạo phải rỗng
        self.assertEqual(0, HistoryList().get_count())

    def test_history_limits_max_size_and_removes_oldest_items(self):
        # Khi vượt MAX_HISTORY_SIZE, các item cũ nhất phải bị loại bỏ
        history = HistoryList()

        for index in range(AppConfig.MAX_HISTORY_SIZE + 3):
            history.add(f"word{index}")

        self.assertEqual(AppConfig.MAX_HISTORY_SIZE, history.get_count())
        self.assertEqual("word3", history.get_item(0))

    def test_history_clears(self):
        # clear phải xóa toàn bộ lịch sử
        history = HistoryList()
        history.add("hello")

        history.clear()

        self.assertEqual([], history.to_list())
