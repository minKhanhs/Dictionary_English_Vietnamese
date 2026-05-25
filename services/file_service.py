import os

from config.app_config import AppConfig
from models.word import Word
from utils.string_utils import StringUtils
from validation.validator import Validator


class FileService:
    """Read and write dictionary data from text files."""

    def ensure_data_folder(self):
        os.makedirs(AppConfig.DATA_FOLDER, exist_ok=True)
        for path in (
            AppConfig.DICTIONARY_FILE,
            AppConfig.HISTORY_FILE,
            AppConfig.FAVORITES_FILE,
        ):
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8"):
                    pass

    def load_dictionary(self):
        self.ensure_data_folder()
        words = []
        try:
            with open(AppConfig.DICTIONARY_FILE, "r", encoding="utf-8") as file:
                for line in file:
                    if not Validator.is_valid_dictionary_line(line):
                        continue
                    word = Word.from_file_line(line)
                    if word is not None:
                        words.append(word)
        except OSError as error:
            print("Could not load dictionary:", error)
        return words

    def save_dictionary(self, words):
        self.ensure_data_folder()
        iterable = words.to_list() if hasattr(words, "to_list") else words
        try:
            with open(AppConfig.DICTIONARY_FILE, "w", encoding="utf-8") as file:
                for word in iterable:
                    file.write(word.to_file_line() + "\n")
            return True
        except OSError as error:
            print("Could not save dictionary:", error)
            return False

    def load_history(self):
        return self._load_words(AppConfig.HISTORY_FILE)

    def save_history(self, history):
        return self._save_words(AppConfig.HISTORY_FILE, history)

    def load_favorites(self):
        return self._load_words(AppConfig.FAVORITES_FILE)

    def save_favorites(self, favorites):
        return self._save_words(AppConfig.FAVORITES_FILE, favorites)

    def _load_words(self, path):
        self.ensure_data_folder()
        items = []
        try:
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    item = StringUtils.normalize_word(line)
                    if item:
                        items.append(item)
        except OSError as error:
            print("Could not load file:", error)
        return items

    def _save_words(self, path, values):
        self.ensure_data_folder()
        iterable = values.to_list() if hasattr(values, "to_list") else values
        try:
            with open(path, "w", encoding="utf-8") as file:
                for item in iterable:
                    normalized = StringUtils.normalize_word(item)
                    if normalized:
                        file.write(normalized + "\n")
            return True
        except OSError as error:
            print("Could not save file:", error)
            return False
