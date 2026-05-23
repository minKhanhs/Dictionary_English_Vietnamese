import unittest

from models.favorite_list import FavoriteList


class FavoriteListTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra danh sách từ yêu thích
    """
    def test_add_favorite_succeeds(self):
        # Thêm một từ hợp lệ vào favorites phải thành công
        self.assertTrue(FavoriteList().add("hello"))

    def test_add_duplicate_favorite_is_rejected(self):
        # Không được thêm trùng một từ đã có trong favorites
        favorites = FavoriteList()

        favorites.add("hello")

        self.assertFalse(favorites.add("hello"))

    def test_contains_finds_existing_favorite(self):
        # contains phải nhận ra từ đã được thêm
        favorites = FavoriteList()

        favorites.add("hello")

        self.assertTrue(favorites.contains("hello"))

    def test_count_tracks_favorites(self):
        # Số lượng favorites phải tăng đúng sau khi thêm
        favorites = FavoriteList()

        favorites.add("hello")

        self.assertEqual(1, favorites.get_count())

    def test_remove_existing_favorite_succeeds(self):
        # Xóa từ đang tồn tại phải thành công và từ đó không còn trong favorites
        favorites = FavoriteList()
        favorites.add("hello")

        self.assertTrue(favorites.remove("hello"))
        self.assertFalse(favorites.contains("hello"))

    def test_remove_missing_favorite_is_rejected(self):
        # Xóa từ không tồn tại phải trả về False
        self.assertFalse(FavoriteList().remove("hello"))
