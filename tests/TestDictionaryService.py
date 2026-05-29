# Test DictionaryService - Kiểm tra nghiệp vụ CRUD từ điển

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.AppConfig import AppConfig
from models.Word import Word
from services.DictionaryService import DictionaryService
from services.FileService import FileService


class TestDictionaryService(unittest.TestCase):
    """Test Suite: Kiểm tra DictionaryService (CRUD, search, history, favorites)"""

    def setUp(self):
        """Tạo service rỗng và thêm vài từ ban đầu"""
        self.service = DictionaryService()
        self.sample_words = [
            Word("hello", "Xin chào", "Hello, how are you?", ["hi", "hey"]),
            Word("world", "Thế giới", "The world is beautiful.", []),
            Word("cat", "Con mèo", "The cat is sleeping.", ["kitty"]),
            Word("dog", "Con chó", "The dog is barking.", ["puppy"]),
            Word("book", "Quyển sách", "I read a book.", []),
        ]
        for word in self.sample_words:
            self.service.add_word_object(word)

    # --- CREATE ---

    def test_add_word_success(self):
        """Thêm từ mới thành công"""
        word = Word("computer", "Máy tính", "I use a computer.", [])
        result = self.service.add_word_object(word)
        self.assertTrue(result)
        self.assertTrue(self.service.word_exists("computer"))

    def test_add_word_duplicate_rejected(self):
        """Không thêm từ trùng"""
        word = Word("hello", "Nghĩa khác", "Example khác", [])
        result = self.service.add_word_object(word)
        self.assertFalse(result)

    def test_add_word_empty_english_rejected(self):
        """Không thêm từ tiếng Anh rỗng"""
        word = Word("", "Nghĩa", "Ví dụ", [])
        self.assertFalse(self.service.add_word_object(word))

    def test_add_word_invalid_english_rejected(self):
        """Không thêm từ tiếng Anh có số"""
        word = Word("hello123", "Nghĩa", "Ví dụ", [])
        self.assertFalse(self.service.add_word_object(word))

    def test_add_word_none_rejected(self):
        """Không thêm None"""
        self.assertFalse(self.service.add_word_object(None))

    # --- READ ---

    def test_word_exists_true(self):
        """Từ tồn tại trong từ điển"""
        self.assertTrue(self.service.word_exists("hello"))
        self.assertTrue(self.service.word_exists("cat"))

    def test_word_exists_false(self):
        """Từ không tồn tại"""
        self.assertFalse(self.service.word_exists("xyz"))
        self.assertFalse(self.service.word_exists(""))

    def test_word_exists_case_insensitive(self):
        """Kiểm tra tồn tại không phân biệt hoa thường"""
        self.assertTrue(self.service.word_exists("HELLO"))
        self.assertTrue(self.service.word_exists("Hello"))

    def test_search_exact_found(self):
        """Tìm chính xác thành công"""
        result = self.service.search_exact("hello")
        self.assertIsNotNone(result)
        self.assertEqual(result.get_english(), "hello")
        self.assertEqual(result.get_vietnamese(), "Xin chào")

    def test_search_exact_not_found(self):
        """Tìm chính xác thất bại"""
        result = self.service.search_exact("xyz")
        self.assertIsNone(result)

    def test_search_exact_empty_string(self):
        """Tìm chuỗi rỗng trả về None"""
        result = self.service.search_exact("")
        self.assertIsNone(result)

    def test_search_exact_adds_to_history(self):
        """Tìm thành công → thêm vào lịch sử"""
        self.service.search_exact("hello")
        self.assertEqual(self.service.history.get_count(), 1)
        self.assertEqual(self.service.history.get_item(0), "hello")

    def test_search_exact_miss_no_history(self):
        """Tìm thất bại → không thêm vào lịch sử"""
        self.service.search_exact("xyz")
        self.assertEqual(self.service.history.get_count(), 0)

    def test_search_approximate_found(self):
        """Tìm gần đúng trả về kết quả"""
        # "helo" gần "hello" (1 lỗi), độ dài 4 → threshold = 1
        results = self.service.search_approximate("helo")
        english_list = [w.get_english() for w in results]
        self.assertIn("hello", english_list)

    def test_search_approximate_no_match(self):
        """Tìm gần đúng không có kết quả"""
        results = self.service.search_approximate("xyz")
        self.assertEqual(len(results), 0)

    def test_search_approximate_empty(self):
        """Tìm gần đúng chuỗi rỗng trả về []"""
        results = self.service.search_approximate("")
        self.assertEqual(results, [])

    def test_search_approximate_max_suggestions(self):
        """Kết quả không vượt quá MAX_SUGGESTIONS"""
        results = self.service.search_approximate("hel")
        self.assertTrue(len(results) <= AppConfig.MAX_SUGGESTIONS)

    # --- UPDATE (synonym) ---

    def test_add_synonym_via_word_object(self):
        """Thêm synonym trực tiếp vào Word object"""
        word = self.service.search_exact("book")
        self.assertIsNotNone(word)
        result = word.add_synonym("volume")
        self.assertTrue(result)
        self.assertTrue(word.has_synonym("volume"))

    # --- DELETE ---

    def test_delete_word_success(self):
        """Xóa từ thành công"""
        result = self.service.delete_word("hello")
        self.assertTrue(result)
        self.assertFalse(self.service.word_exists("hello"))
        # Kiểm tra ArrayList size giảm
        found = self.service._find_word("hello")
        self.assertIsNone(found)

    def test_delete_word_not_found(self):
        """Xóa từ không tồn tại"""
        result = self.service.delete_word("xyz")
        self.assertFalse(result)

    def test_delete_word_empty(self):
        """Xóa từ rỗng"""
        result = self.service.delete_word("")
        self.assertFalse(result)

    def test_delete_word_removes_from_favorites(self):
        """Xóa từ cũng xóa khỏi favorites nếu có"""
        self.service.favorites.add("cat")
        self.assertTrue(self.service.favorites.contains("cat"))
        self.service.delete_word("cat")
        self.assertFalse(self.service.favorites.contains("cat"))

    def test_delete_preserves_other_words(self):
        """Xóa một từ không ảnh hưởng từ khác"""
        self.service.delete_word("cat")
        self.assertTrue(self.service.word_exists("hello"))
        self.assertTrue(self.service.word_exists("dog"))
        self.assertTrue(self.service.word_exists("book"))

    # --- HISTORY ---

    def test_history_tracks_searches(self):
        """Lịch sử theo dõi các từ đã tra"""
        self.service.search_exact("hello")
        self.service.search_exact("cat")
        self.assertEqual(self.service.history.get_count(), 2)

    # --- FAVORITES ---

    def test_favorites_add_and_contains(self):
        """Thêm và kiểm tra favorites"""
        self.service.favorites.add("hello")
        self.assertTrue(self.service.favorites.contains("hello"))

    def test_favorites_remove(self):
        """Xóa khỏi favorites"""
        self.service.favorites.add("hello")
        self.service.favorites.remove("hello")
        self.assertFalse(self.service.favorites.contains("hello"))

    def test_favorites_no_duplicate(self):
        """Không thêm trùng favorites"""
        self.service.favorites.add("hello")
        result = self.service.favorites.add("hello")
        self.assertFalse(result)

    # --- DISPLAY (không test output, chỉ test không crash) ---

    def test_display_all_words_no_crash(self):
        """display_all_words không crash"""
        self.service.display_all_words()

    def test_show_history_no_crash(self):
        """show_history không crash"""
        self.service.show_history()

    def test_show_favorites_no_crash(self):
        """show_favorites không crash"""
        self.service.show_favorites()


if __name__ == "__main__":
    unittest.main()
