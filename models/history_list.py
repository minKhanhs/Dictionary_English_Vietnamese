from config.app_config import AppConfig
from utils.string_utils import StringUtils


class HistoryList:
    """Recent lookup history with a fixed maximum size."""

    def __init__(self):
        self.items = []
        self.count = 0

    def add(self, word):
        normalized = StringUtils.normalize_word(word)
        if not normalized:
            return False
        self.items.append(normalized)
        if len(self.items) > AppConfig.MAX_HISTORY_SIZE:
            self.items.pop(0)
        self.count = len(self.items)
        return True

    def display(self):
        if not self.items:
            print("History is empty.")
            return
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item}")

    def get_count(self):
        return self.count

    def get_item(self, index):
        if index < 0 or index >= self.count:
            return None
        return self.items[index]

    def clear(self):
        self.items = []
        self.count = 0

    def to_list(self):
        return list(self.items)
