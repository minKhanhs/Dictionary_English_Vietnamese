"""Central response metadata for the local test suites."""


class ResponseCode:
    """Standard status codes used when reporting test responses."""

    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"

    PASS_LABEL = f"[{PASS}]"
    FAIL_LABEL = f"[{FAIL}]"
    SKIP_LABEL = f"[{SKIP}]"


TEST_RESPONSES = {
    "word_test.py": {
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
    "trie_test.py": {
        "docstring": "Validate Trie insert, exact search, missing search, and prefix lookup behavior.",
        "tests": [
            "trie finds inserted word",
            "trie returns None when missing",
            "trie detects prefix",
            "trie rejects missing prefix",
        ],
    },
    "levenshtein_test.py": {
        "docstring": "Validate Levenshtein distance operations and threshold selection.",
        "tests": [
            "same word",
            "one insertion",
            "one deletion",
            "one substitution",
            "kitten sitting",
            "short threshold",
        ],
    },
    "validator_test.py": {
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
    "dynamic_array_test.py": {
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
    "history_list_test.py": {
        "docstring": "Validate HistoryList count, maximum size trimming, item order, and clearing.",
        "tests": [
            "history starts empty",
            "history max size",
            "history removes oldest",
            "history clears",
        ],
    },
    "favorite_list_test.py": {
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
    "file_service_test.py": {
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
    "dictionary_service_test.py": {
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
    "TestFuzzySearch.py": {
        "docstring": "Validate the new Levenshtein row-based helper and FuzzySearch suggestion behavior.",
        "tests": [
            "testGetInitialRow",
            "testCalculateNextRowMatch",
            "testCalculateNextRowMismatch",
            "testGetMaxDistanceLogic",
            "testExactMatch",
            "testTypoMatchShortWord",
            "testExceedMaxDistance",
            "testMaxSuggestionsLimit",
            "testEmptyString",
        ],
    },
}


def get_test_response(file_name):
    """Return response metadata for one test file."""
    return TEST_RESPONSES.get(file_name)


def list_test_files():
    """Return all test files that have response metadata."""
    return list(TEST_RESPONSES.keys())
