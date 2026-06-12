import os


class AppConfig:
    DATA_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DICTIONARY_FILE = os.path.join(DATA_FOLDER, "dictionary.txt")
    HISTORY_FILE = os.path.join(DATA_FOLDER, "history.txt")
    FAVORITES_FILE = os.path.join(DATA_FOLDER, "favorites.txt")

    MAX_SYNONYMS = 10
    MAX_HISTORY_SIZE = 20
    MAX_SUGGESTIONS = 5

    # Cấu hình cho Trie: chỉ xử lý chữ cái tiếng Anh a-z.
    ALPHABET_SIZE = 26
    FIRST_CHAR = "a"
    LAST_CHAR = "z"

    # Cấu hình ngưỡng khoảng cách Levenshtein
    SHORT_WORD_LENGTH = 4
    MEDIUM_WORD_LENGTH = 8
    SHORT_WORD_DISTANCE = 1
    MEDIUM_WORD_DISTANCE = 2
    LONG_WORD_DISTANCE = 3

    # Định dạng dữ liệu file
    FIELD_SEPARATOR = "|"
    LIST_SEPARATOR = ","
    DICTIONARY_FILE_FIELD_COUNT = 4

    # Giới hạn độ dài dữ liệu để validation
    MIN_WORD_LENGTH = 1
    MAX_WORD_LENGTH = 50
    MIN_MEANING_LENGTH = 1
    MAX_MEANING_LENGTH = 200
    MIN_EXAMPLE_LENGTH = 1
    MAX_EXAMPLE_LENGTH = 500

    # Lựa chọn Menu
    MIN_MENU_OPTION = 0
    MAX_MENU_OPTION = 11
