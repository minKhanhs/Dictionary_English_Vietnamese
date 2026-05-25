import unittest

from models.word import Word
from services.dictionary_service import DictionaryService


class FakeFileService:
    def __init__(self):
        self.dictionary = []
        self.history = []
        self.favorites = []

    def load_dictionary(self):
        return list(self.dictionary)

    def save_dictionary(self, words):
        self.dictionary = words.to_list()
        return True

    def load_history(self):
        return list(self.history)

    def save_history(self, history):
        self.history = history.to_list()
        return True

    def load_favorites(self):
        return list(self.favorites)

    def save_favorites(self, favorites):
        self.favorites = favorites.to_list()
        return True


class DictionaryServiceTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra service quản lý từ điển ở tầng nghiệp vụ
    """
    def setUp(self):
        # Dùng FakeFileService để test không phụ thuộc vào file thật
        self.service = DictionaryService(FakeFileService())

    def test_service_adds_new_word(self):
        # Thêm một từ hợp lệ phải thành công
        self.assertTrue(self.service.add_word_object(Word("hello", "xin chao")))

    def test_service_rejects_duplicate_word(self):
        # Thêm lại cùng một từ phải bị từ chối
        self.service.add_word_object(Word("hello", "xin chao"))

        self.assertFalse(self.service.add_word_object(Word("hello", "xin chao")))

    def test_service_rejects_empty_word(self):
        # Từ tiếng Anh rỗng không được thêm vào từ điển
        self.assertFalse(self.service.add_word_object(Word("", "rong")))

    def test_service_rejects_number_in_word(self):
        # Từ tiếng Anh chứa số phải bị validation từ chối
        self.assertFalse(self.service.add_word_object(Word("hello2", "sai")))

    def test_exact_search_finds_word_and_adds_history(self):
        # Tra cứu chính xác phải trả về từ và đồng thời thêm vào history
        self.service.add_word_object(Word("hello", "xin chao"))

        self.assertEqual("hello", self.service.search_exact("hello").get_english())
        self.assertEqual(1, self.service.history.get_count())

    def test_approximate_search_returns_suggestions(self):
        # Khi nhập sai gần đúng, service phải trả về ít nhất một gợi ý
        self.service.add_word_object(Word("hello", "xin chao"))
        self.service.add_word_object(Word("help", "giup do"))

        self.assertGreater(len(self.service.search_approximate("helo")), 0)

    def test_favorite_rejects_empty_word(self):
        # Favorites không nhận từ rỗng
        self.assertFalse(self.service.favorites.add(""))

    def test_favorite_core_add_succeeds(self):
        # Thêm từ hợp lệ vào favorites phải thành công
        self.assertTrue(self.service.favorites.add("hello"))

    def test_word_exists_for_existing_word(self):
        # word_exists phải trả về True với từ đã có trong từ điển
        self.service.add_word_object(Word("hello", "xin chao"))

        self.assertTrue(self.service.word_exists("hello"))

    def test_service_saves_data(self):
        # save_data phải gọi được xuống file service và trả về True
        self.assertTrue(self.service.save_data())
