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


class DictionaryServiceTest:
    @staticmethod
    def run(runner):
        service = DictionaryService(FakeFileService())
        runner.assert_true(
            service.add_word_object(Word("hello", "xin chao")),
            "service adds new word",
        )
        runner.assert_false(
            service.add_word_object(Word("hello", "xin chao")),
            "service rejects duplicate word",
        )
        runner.assert_false(
            service.add_word_object(Word("", "rong")),
            "service rejects empty word",
        )
        runner.assert_false(
            service.add_word_object(Word("hello2", "sai")),
            "service rejects number in word",
        )
        runner.assert_equal("hello", service.search_exact("hello").get_english(), "service exact search")
        runner.assert_equal(1, service.history.get_count(), "exact search adds history")
        service.add_word_object(Word("help", "giup do"))
        runner.assert_true(
            len(service.search_approximate("helo")) > 0,
            "service approximate suggestions",
        )
        runner.assert_false(service.favorites.add(""), "favorite rejects empty")
        runner.assert_true(service.favorites.add("hello"), "favorite core add")
        runner.assert_true(service.word_exists("hello"), "word exists")
        runner.assert_true(service.save_data(), "service saves data")
