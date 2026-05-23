"""Central response metadata for the local unittest suites."""


class ResponseCode:
    """Standard status codes used when reporting test responses."""

    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"

    PASS_LABEL = f"[{PASS}]"
    FAIL_LABEL = f"[{FAIL}]"
    SKIP_LABEL = f"[{SKIP}]"


TEST_RESPONSES = {
    "test_word.py": {
        "docstring": "Validate Word normalization, synonym handling, file serialization, and bad input parsing.",
        "tests": [
            "word normalizes english",
            "add synonym succeeds",
            "duplicate synonym rejected",
            "synonym count is correct",
            "word round trip english",
            "word round trip meaning",
            "word round trip synonym",
            "word limits synonyms",
            "bad line returns None",
        ],
    },
    "test_trie.py": {
        "docstring": "Validate Trie insert, exact search, missing search, and prefix lookup behavior.",
        "tests": [
            "trie finds inserted word",
            "trie returns None when missing",
            "trie detects prefix",
            "trie rejects missing prefix",
        ],
    },
    "test_levenshtein.py": {
        "docstring": "Validate Levenshtein distance operations and row calculation helpers.",
        "tests": [
            "test_distance_for_same_word_is_zero",
            "test_distance_handles_one_insertion",
            "test_distance_handles_one_deletion",
            "test_distance_handles_one_substitution",
            "test_distance_handles_multiple_edits",
            "test_initial_row_matches_target_word_length",
            "test_calculate_next_row_for_matching_character",
            "test_calculate_next_row_for_mismatching_character",
        ],
    },
    "test_validator.py": {
        "docstring": "Validate empty checks, English words, Vietnamese meanings, menu choices, and dictionary lines.",
        "tests": [
            "empty spaces detected",
            "valid spaces",
            "valid hyphen",
            "word with number rejected",
            "empty word rejected",
            "meaning accepted",
            "menu choice max accepted",
            "menu text rejected",
            "dictionary line accepted",
            "short dictionary line rejected",
        ],
    },
    "test_dynamic_array.py": {
        "docstring": "Validate DynamicArray growth, indexing, updates, removal, conversion, and clearing.",
        "tests": [
            "array starts empty",
            "array grows size",
            "array resizes capacity",
            "array get works",
            "array set works",
            "array remove returns item",
            "array shifts after remove",
            "array clears",
        ],
    },
    "test_history_list.py": {
        "docstring": "Validate HistoryList count, maximum size trimming, item order, and clearing.",
        "tests": [
            "history starts empty",
            "history max size",
            "history removes oldest",
            "history clears",
        ],
    },
    "test_favorite_list.py": {
        "docstring": "Validate FavoriteList add, duplicate handling, contains, count, removal, and missing removal.",
        "tests": [
            "favorite add succeeds",
            "favorite duplicate rejected",
            "favorite contains word",
            "favorite count",
            "favorite remove succeeds",
            "favorite no longer contains",
            "favorite remove missing rejected",
        ],
    },
    "test_file_service.py": {
        "docstring": "Validate file creation, dictionary/history/favorites loading, saving, and round trips.",
        "tests": [
            "file service creates dictionary",
            "missing dictionary loads empty",
            "bad dictionary line skipped",
            "dictionary saves",
            "dictionary round trip",
            "history saves",
            "history round trip",
            "favorites saves",
            "favorites round trip",
        ],
    },
    "test_dictionary_service.py": {
        "docstring": "Validate DictionaryService add, duplicate rejection, validation, exact and approximate search, favorites, existence, and persistence.",
        "tests": [
            "service adds new word",
            "service rejects duplicate word",
            "service rejects empty word",
            "service rejects number in word",
            "service exact search",
            "exact search adds history",
            "service approximate suggestions",
            "favorite rejects empty",
            "favorite core add",
            "word exists",
            "service saves data",
        ],
    },
    "test_fuzzy_search.py": {
        "docstring": "Validate FuzzySearch distance thresholds and suggestion behavior.",
        "tests": [
            "test_get_max_distance_uses_config_thresholds",
            "test_exact_match_is_first_suggestion",
            "test_typo_match_for_short_word_returns_close_words",
            "test_word_exceeding_max_distance_returns_no_suggestions",
            "test_suggestions_do_not_exceed_config_limit",
            "test_empty_string_returns_empty_list",
        ],
    },
}


def get_test_response(file_name):
    """Return response metadata for one test file."""
    return TEST_RESPONSES.get(file_name)


def list_test_files():
    """Return all test files that have response metadata."""
    return list(TEST_RESPONSES.keys())
