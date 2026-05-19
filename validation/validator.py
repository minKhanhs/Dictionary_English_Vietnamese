from config.app_config import AppConfig
from utils.string_utils import StringUtils


class Validator:
    """Input and file-format validation helpers."""

    @staticmethod
    def is_empty(value):
        return value is None or len(str(value).strip()) == 0

    @staticmethod
    def is_length_in_range(value, min_length, max_length):
        if value is None:
            return False
        length = len(str(value))
        return min_length <= length <= max_length

    @staticmethod
    def is_valid_english_word(word):
        normalized = StringUtils.normalize_word(word)
        if not Validator.is_length_in_range(
            normalized, AppConfig.MIN_WORD_LENGTH, AppConfig.MAX_WORD_LENGTH
        ):
            return False
        for char in normalized:
            if not ("a" <= char <= "z" or char in (" ", "-")):
                return False
        return True

    @staticmethod
    def is_valid_vietnamese_meaning(meaning):
        cleaned = StringUtils.trim(meaning)
        return Validator.is_length_in_range(
            cleaned, AppConfig.MIN_MEANING_LENGTH, AppConfig.MAX_MEANING_LENGTH
        )

    @staticmethod
    def is_valid_example(example):
        cleaned = StringUtils.trim(example)
        return Validator.is_length_in_range(
            cleaned, AppConfig.MIN_EXAMPLE_LENGTH, AppConfig.MAX_EXAMPLE_LENGTH
        )

    @staticmethod
    def is_valid_synonym(synonym):
        return Validator.is_valid_english_word(synonym)

    @staticmethod
    def is_valid_menu_choice(choice, min_choice=None, max_choice=None):
        if Validator.is_empty(choice):
            return False
        minimum = AppConfig.MIN_MENU_OPTION if min_choice is None else min_choice
        maximum = AppConfig.MAX_MENU_OPTION if max_choice is None else max_choice
        try:
            value = int(choice)
        except (TypeError, ValueError):
            return False
        return minimum <= value <= maximum

    @staticmethod
    def has_enough_fields(line, separator, expected_fields):
        if line is None:
            return False
        return len(str(line).rstrip("\n").split(separator)) >= expected_fields

    @staticmethod
    def is_valid_dictionary_line(line):
        if not Validator.has_enough_fields(
            line, AppConfig.FIELD_SEPARATOR, AppConfig.DICTIONARY_FILE_FIELD_COUNT
        ):
            return False
        parts = str(line).rstrip("\n").split(AppConfig.FIELD_SEPARATOR)
        return Validator.is_valid_english_word(
            parts[0]
        ) and Validator.is_valid_vietnamese_meaning(parts[1])
