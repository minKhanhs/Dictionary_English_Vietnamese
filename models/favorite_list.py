from utils.string_utils import StringUtils


class FavoriteList:
    """Stores favorite words without duplicates."""

    def __init__(self):
        self.favorites = []

    def add(self, word):
        normalized = StringUtils.normalize_word(word)
        if not normalized or self.contains(normalized):
            return False
        self.favorites.append(normalized)
        return True

    def remove(self, word):
        normalized = StringUtils.normalize_word(word)
        if not self.contains(normalized):
            return False
        self.favorites.remove(normalized)
        return True

    def contains(self, word):
        return StringUtils.normalize_word(word) in self.favorites

    def display(self):
        if not self.favorites:
            print("Favorites is empty.")
            return
        for index, item in enumerate(self.favorites, start=1):
            print(f"{index}. {item}")

    def get_count(self):
        return len(self.favorites)

    def get_item(self, index):
        if index < 0 or index >= len(self.favorites):
            return None
        return self.favorites[index]

    def clear(self):
        self.favorites = []

    def to_list(self):
        return list(self.favorites)
