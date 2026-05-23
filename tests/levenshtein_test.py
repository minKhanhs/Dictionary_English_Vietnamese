from algorithms.Levenshtein import Levenshtein
from algorithms.FuzzySearch import FuzzySearch
from config.app_config import AppConfig


class EmptyFuzzyTrieNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False


class LevenshteinTest:
    @staticmethod
    def run(runner):
        runner.assert_equal(0, Levenshtein("hello").distance("hello"), "same word")
        runner.assert_equal(1, Levenshtein("hello").distance("helo"), "one insertion")
        runner.assert_equal(1, Levenshtein("helo").distance("hello"), "one deletion")
        runner.assert_equal(1, Levenshtein("cat").distance("cut"), "one substitution")
        runner.assert_equal(3, Levenshtein("kitten").distance("sitting"), "kitten sitting")

        matcher = FuzzySearch(EmptyFuzzyTrieNode())
        runner.assert_equal(
            AppConfig.SHORT_WORD_DISTANCE,
            matcher.getMaxDistance(AppConfig.SHORT_WORD_LENGTH),
            "short threshold",
        )
