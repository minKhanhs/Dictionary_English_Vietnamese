class AppConfig:
    """Central configuration for the dictionary application."""

    DATA_FOLDER = "data"
    DICTIONARY_FILE = "data/dictionary.txt"
    HISTORY_FILE = "data/history.txt"
    FAVORITES_FILE = "data/favorites.txt"

    MAX_SYNONYMS = 10
    MAX_HISTORY_SIZE = 20
    MAX_SUGGESTIONS = 5

    ALPHABET_SIZE = 26
    FIRST_CHAR = "a"
    LAST_CHAR = "z"

    SHORT_WORD_LENGTH = 4
    MEDIUM_WORD_LENGTH = 8
    SHORT_WORD_DISTANCE = 1
    MEDIUM_WORD_DISTANCE = 2
    LONG_WORD_DISTANCE = 3

    FIELD_SEPARATOR = "|"
    LIST_SEPARATOR = ","

    MIN_WORD_LENGTH = 1
    MAX_WORD_LENGTH = 50
    MIN_MEANING_LENGTH = 1
    MAX_MEANING_LENGTH = 200
    MIN_EXAMPLE_LENGTH = 0
    MAX_EXAMPLE_LENGTH = 500
    MIN_MENU_OPTION = 0
    MAX_MENU_OPTION = 10
    DICTIONARY_FILE_FIELD_COUNT = 4
