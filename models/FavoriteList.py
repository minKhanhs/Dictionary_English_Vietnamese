# Model FavoriteList - Quản lý danh sách từ yêu thích

from utils.StringUtils import StringUtils


class FavoriteList:
    """Danh sách từ yêu thích, không cho thêm trùng."""

    def __init__(self):
        self.favorites = []

    def add(self, word):
        """Thêm từ yêu thích. Trả về False nếu trùng hoặc rỗng."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return False
        if self.contains(normalized):
            return False
        self.favorites.append(normalized)
        return True

    def remove(self, word):
        """Xóa từ yêu thích. Trả về False nếu không tìm thấy."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not self.contains(normalized):
            return False
        self.favorites.remove(normalized)
        return True

    def contains(self, word):
        """Kiểm tra từ đã có trong favorites chưa."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        return normalized in self.favorites

    def display(self):
        """In danh sách yêu thích ra console."""
        if not self.favorites:
            print("Danh sách yêu thích trống.")
            return
        for index, item in enumerate(self.favorites, start=1):
            print(f"{index}. {item}")

    def get_count(self):
        return len(self.favorites)

    def get_item(self, index):
        """Lấy mục tại vị trí index. Trả về None nếu ngoài phạm vi."""
        if index < 0 or index >= len(self.favorites):
            return None
        return self.favorites[index]

    def clear(self):
        """Xóa toàn bộ danh sách yêu thích."""
        self.favorites = []

    def to_list(self):
        """Trả về bản sao danh sách."""
        return list(self.favorites)
