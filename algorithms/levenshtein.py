from config.app_config import AppConfig
from utils.string_utils import StringUtils


class Levenshtein:
    """Self-contained Levenshtein distance implementation."""

    @staticmethod
    def distance(a, b):
        first = StringUtils.normalize_word(a)
        second = StringUtils.normalize_word(b)
        rows = len(first) + 1
        cols = len(second) + 1
        matrix = [[0] * cols for _ in range(rows)]

        for row in range(rows):
            matrix[row][0] = row
        for col in range(cols):
            matrix[0][col] = col

        for row in range(1, rows):
            for col in range(1, cols):
                cost = 0 if first[row - 1] == second[col - 1] else 1
                matrix[row][col] = min(
                    matrix[row - 1][col] + 1,
                    matrix[row][col - 1] + 1,
                    matrix[row - 1][col - 1] + cost,
                )
        return matrix[-1][-1]

    @staticmethod
    def get_threshold(word_length):
        if word_length <= AppConfig.SHORT_WORD_LENGTH:
            return AppConfig.SHORT_WORD_DISTANCE
        if word_length <= AppConfig.MEDIUM_WORD_LENGTH:
            return AppConfig.MEDIUM_WORD_DISTANCE
        return AppConfig.LONG_WORD_DISTANCE
