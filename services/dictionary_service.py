from algorithms.levenshtein import Levenshtein
from config.app_config import AppConfig
from models.favorite_list import FavoriteList
from models.history_list import HistoryList
from models.word import Word
from services.file_service import FileService
from structures.dynamic_array import DynamicArray
from structures.trie import Trie
from utils.string_utils import StringUtils
from validation.validator import Validator


class DictionaryService:
    """Business logic for dictionary CRUD, search, history, and favorites."""

    def __init__(self, file_service=None):
        self.trie = Trie()
        self.words = DynamicArray()
        self.history = HistoryList()
        self.favorites = FavoriteList()
        self.file_service = file_service or FileService()

    def load_data(self):
        self.trie = Trie()
        self.words = DynamicArray()
        self.history.clear()
        self.favorites.clear()

        for word in self.file_service.load_dictionary():
            self.words.push_back(word)
            self.trie.insert(word)
        for item in self.file_service.load_history():
            self.history.add(item)
        for item in self.file_service.load_favorites():
            self.favorites.add(item)

    def save_data(self):
        dictionary_saved = self.file_service.save_dictionary(self.words)
        history_saved = self.file_service.save_history(self.history)
        favorites_saved = self.file_service.save_favorites(self.favorites)
        return dictionary_saved and history_saved and favorites_saved

    def add_word_object(self, word):
        if word is None:
            return False
        if not Validator.is_valid_english_word(word.get_english()):
            return False
        if not Validator.is_valid_vietnamese_meaning(word.get_vietnamese()):
            return False
        if not Validator.is_valid_example(word.get_example()):
            return False
        if self.word_exists(word.get_english()):
            return False
        self.words.push_back(word)
        self.trie.insert(word)
        return True

    def word_exists(self, word):
        return self.trie.search(word) is not None

    def search_exact(self, word):
        normalized = StringUtils.normalize_word(word)
        result = self.trie.search(normalized)
        if result is not None:
            self.history.add(normalized)
        return result

    def search_approximate(self, word):
        normalized = StringUtils.normalize_word(word)
        if not normalized:
            return []
        threshold = Levenshtein.get_threshold(len(normalized))
        suggestions = []
        for current in self.words.to_list():
            distance = Levenshtein.distance(normalized, current.get_english())
            if distance <= threshold:
                suggestions.append((distance, current))
        suggestions.sort(key=lambda item: (item[0], item[1].get_english()))
        return [item[1] for item in suggestions[: AppConfig.MAX_SUGGESTIONS]]

    def add_word_interactive(self):
        english = input("English word: ")
        vietnamese = input("Vietnamese meaning: ")
        example = input("Example: ")
        synonyms_input = input("Synonyms separated by comma (optional): ")
        synonyms = [
            item
            for item in StringUtils.split(synonyms_input, AppConfig.LIST_SEPARATOR)
            if StringUtils.trim(item)
        ]
        word = Word(english, vietnamese, example, synonyms)
        if self.add_word_object(word):
            print("Word added.")
            return True
        print("Could not add word. Please check input or duplicate word.")
        return False

    def add_synonym_interactive(self):
        english = input("English word: ")
        word = self.trie.search(english)
        if word is None:
            print("Word not found.")
            return False
        synonym = input("Synonym: ")
        if word.add_synonym(synonym):
            print("Synonym added.")
            return True
        print("Could not add synonym.")
        return False

    def search_exact_interactive(self):
        english = input("English word: ")
        word = self.search_exact(english)
        if word is not None:
            word.display()
            return word
        print("Word not found.")
        self._display_suggestions(english)
        return None

    def search_approximate_interactive(self):
        english = input("English word: ")
        return self._display_suggestions(english)

    def add_favorite_interactive(self):
        english = input("English word: ")
        normalized = StringUtils.normalize_word(english)
        if not self.word_exists(normalized):
            print("Word must exist before it can be favorited.")
            return False
        if self.favorites.add(normalized):
            print("Favorite added.")
            return True
        print("Favorite already exists.")
        return False

    def remove_favorite_interactive(self):
        english = input("English word: ")
        if self.favorites.remove(english):
            print("Favorite removed.")
            return True
        print("Favorite not found.")
        return False

    def show_history(self):
        self.history.display()

    def show_favorites(self):
        self.favorites.display()

    def display_all_words(self):
        if self.words.is_empty():
            print("Dictionary is empty.")
            return
        for index, word in enumerate(self.words.to_list(), start=1):
            print(f"\n{index}.")
            word.display()

    def _display_suggestions(self, english):
        suggestions = self.search_approximate(english)
        if not suggestions:
            print("No suggestions.")
            return []
        print("Suggestions:")
        for index, word in enumerate(suggestions, start=1):
            print(f"{index}. {word.get_english()} - {word.get_vietnamese()}")
        return suggestions
