from algorithms.levenshtein import Levenshtein
from config.app_config import AppConfig


class LevenshteinTest:
    @staticmethod
    def run(runner):
        runner.assert_equal(0, Levenshtein.distance("hello", "hello"), "same word")
        runner.assert_equal(1, Levenshtein.distance("helo", "hello"), "one insertion")
        runner.assert_equal(1, Levenshtein.distance("hello", "helo"), "one deletion")
        runner.assert_equal(1, Levenshtein.distance("cat", "cut"), "one substitution")
        runner.assert_equal(3, Levenshtein.distance("kitten", "sitting"), "kitten sitting")
        runner.assert_equal(
            AppConfig.SHORT_WORD_DISTANCE,
            Levenshtein.get_threshold(AppConfig.SHORT_WORD_LENGTH),
            "short threshold",
        )
