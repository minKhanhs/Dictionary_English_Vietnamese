from config.app_config import AppConfig
from utils.string_utils import StringUtils
from validation.validator import Validator


class Word:
    """Dictionary entry containing the English word and its metadata."""

    def __init__(self, english="", vietnamese="", example="", synonyms=None):
        self.english = StringUtils.normalize_word(english)
        self.vietnamese = StringUtils.trim(vietnamese)
        self.example = StringUtils.trim(example)
        self.synonyms = []
        if synonyms:
            for synonym in synonyms:
                self.add_synonym(synonym)

    def get_english(self):
        return self.english

    def get_vietnamese(self):
        return self.vietnamese

    def get_example(self):
        return self.example

    def get_synonyms(self):
        return list(self.synonyms)

    def get_synonym_count(self):
        return len(self.synonyms)

    def set_english(self, english):
        self.english = StringUtils.normalize_word(english)

    def set_vietnamese(self, vietnamese):
        self.vietnamese = StringUtils.trim(vietnamese)

    def set_example(self, example):
        self.example = StringUtils.trim(example)

    def add_synonym(self, synonym):
        normalized = StringUtils.normalize_word(synonym)
        if not Validator.is_valid_synonym(normalized):
            return False
        if self.has_synonym(normalized):
            return False
        if len(self.synonyms) >= AppConfig.MAX_SYNONYMS:
            return False
        self.synonyms.append(normalized)
        return True

    def has_synonym(self, synonym):
        normalized = StringUtils.normalize_word(synonym)
        return normalized in self.synonyms

    def display(self):
        print("English:", self.english)
        print("Vietnamese:", self.vietnamese)
        if self.example:
            print("Example:", self.example)
        if self.synonyms:
            print("Synonyms:", StringUtils.join(self.synonyms, ", "))

    def to_file_line(self):
        return AppConfig.FIELD_SEPARATOR.join(
            [
                self.english,
                self.vietnamese,
                self.example,
                StringUtils.join(self.synonyms, AppConfig.LIST_SEPARATOR),
            ]
        )

    @staticmethod
    def from_file_line(line):
        if not Validator.is_valid_dictionary_line(line):
            return None
        parts = str(line).rstrip("\n").split(AppConfig.FIELD_SEPARATOR)
        synonyms = []
        if len(parts) > 3 and parts[3].strip():
            synonyms = [
                item.strip()
                for item in parts[3].split(AppConfig.LIST_SEPARATOR)
                if item.strip()
            ]
        return Word(parts[0], parts[1], parts[2], synonyms)
