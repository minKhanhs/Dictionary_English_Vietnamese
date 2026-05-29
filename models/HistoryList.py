# Model HistoryList - Quản lý lịch sử tra cứu gần đây

from config.AppConfig import AppConfig
from utils.StringUtils import StringUtils


class HistoryList:
    """Danh sách lịch sử tra cứu, giới hạn MAX_HISTORY_SIZE, FIFO eviction."""

    def __init__(self):
        self.items = []
        self.count = 0

    def add(self, word):
        """Thêm từ vào lịch sử. Xóa phần tử cũ nhất nếu vượt giới hạn."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return False
        self.items.append(normalized)
        if len(self.items) > AppConfig.MAX_HISTORY_SIZE:
            self.items.pop(0)
        self.count = len(self.items)
        return True

    def display(self):
        """In lịch sử ra console."""
        if not self.items:
            print("Lịch sử trống.")
            return
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item}")

    def get_count(self):
        return self.count

    def get_item(self, index):
        """Lấy mục tại vị trí index. Trả về None nếu ngoài phạm vi."""
        if index < 0 or index >= self.count:
            return None
        return self.items[index]

    def clear(self):
        """Xóa toàn bộ lịch sử."""
        self.items = []
        self.count = 0

    def to_list(self):
        """Trả về bản sao danh sách."""
        return list(self.items)
