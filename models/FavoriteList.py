from config.ResponseCode import ResponseCode
from utils.StringUtils import StringUtils


class FavoriteList:
    """Danh sách từ yêu thích, không cho thêm trùng."""

    def __init__(self):
        self.favorites = []

    def add(self, word):
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized or self.contains(normalized):
            return False
        self.favorites.append(normalized)
        return True

    def remove(self, word):
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not self.contains(normalized):
            return False
        self.favorites.remove(normalized)
        return True

    def contains(self, word):
        normalized = StringUtils.normalizeWord(word) if word else ""
        return normalized in self.favorites

    def display(self):
        if not self.favorites:
            print(f"[{ResponseCode.EMPTY}] Danh sách yêu thích trống.")
            return
        for index, item in enumerate(self.favorites, start=1):
            print(f"{index}. {item}")

    def getCount(self):
        return len(self.favorites)

    def getItem(self, index):
        if index < 0 or index >= len(self.favorites):
            return None
        return self.favorites[index]

    def clear(self):
        self.favorites = []

    def toList(self):
        return list(self.favorites)
