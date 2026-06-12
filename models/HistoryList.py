from config.AppConfig import AppConfig
from config.ResponseCode import ResponseCode
from utils.StringUtils import StringUtils


class HistoryList:
    """Lịch sử tra cứu, giới hạn MAX_HISTORY_SIZE, FIFO eviction."""

    def __init__(self):
        self.items = []
        self.count = 0

    def add(self, word):
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return False
        self.items.append(normalized)
        while len(self.items) > AppConfig.MAX_HISTORY_SIZE:
            self.items.pop(0)
        self.count = len(self.items)
        return True

    def display(self):
        if not self.items:
            print(f"[{ResponseCode.EMPTY}] Lịch sử trống.")
            return
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item}")

    def getCount(self):
        return self.count

    def getItem(self, index):
        if index < 0 or index >= self.count:
            return None
        return self.items[index]

    def clear(self):
        self.items = []
        self.count = 0

    def toList(self):
        return list(self.items)
