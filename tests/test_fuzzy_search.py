import unittest

from algorithms.FuzzySearch import FuzzySearch
from config.app_config import AppConfig


class FakeFuzzyTrieNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = FakeFuzzyTrieNode()
            node = node.children[char]
        node.isEndOfWord = True


class FuzzySearchTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra logic tìm kiếm gần đúng trên cây Trie
    """
    def setUp(self):
        # 1. Khởi tạo cây Trie giả lập với một nhóm từ mẫu
        self.trie_root = FakeFuzzyTrieNode()
        self.dictionary_words = [
            "hello",
            "hell",
            "helicopter",
            "hero",
            "help",
            "healer",
            "halo",
            "cat",
            "car",
        ]
        for word in self.dictionary_words:
            self.trie_root.insert(word)

        # 2. Khởi tạo bộ tìm kiếm gần đúng
        self.matcher = FuzzySearch(self.trie_root)

    def test_get_max_distance_uses_config_thresholds(self):
        # Kiểm tra hàm lấy ngưỡng khoảng cách có tuân thủ AppConfig không
        # Từ ngắn dùng SHORT_WORD_DISTANCE, từ trung bình dùng MEDIUM_WORD_DISTANCE
        self.assertEqual(AppConfig.SHORT_WORD_DISTANCE, self.matcher.getMaxDistance(3))
        self.assertEqual(AppConfig.SHORT_WORD_DISTANCE, self.matcher.getMaxDistance(4))
        self.assertEqual(AppConfig.MEDIUM_WORD_DISTANCE, self.matcher.getMaxDistance(6))

    def test_exact_match_is_first_suggestion(self):
        # Nếu nhập đúng từ có trong từ điển, nó phải nằm đầu danh sách gợi ý
        suggestions = self.matcher.getSuggestions("hello")

        self.assertGreater(len(suggestions), 0)
        self.assertEqual("hello", suggestions[0])

    def test_typo_match_for_short_word_returns_close_words(self):
        # Từ "helo" sai 1 lỗi, nên các từ gần như "hello" và "hell" phải được gợi ý
        suggestions = self.matcher.getSuggestions("helo")

        self.assertIn("hello", suggestions)
        self.assertIn("hell", suggestions)

    def test_word_exceeding_max_distance_returns_no_suggestions(self):
        # Từ "xyz" quá khác các từ trong Trie, nên không có gợi ý phù hợp
        self.assertEqual([], self.matcher.getSuggestions("xyz"))

    def test_suggestions_do_not_exceed_config_limit(self):
        # Danh sách kết quả không được vượt quá MAX_SUGGESTIONS trong AppConfig
        suggestions = self.matcher.getSuggestions("hel")

        self.assertLessEqual(len(suggestions), AppConfig.MAX_SUGGESTIONS)

    def test_empty_string_returns_empty_list(self):
        # Chuỗi rỗng phải trả về danh sách rỗng và không gây lỗi
        self.assertEqual([], self.matcher.getSuggestions(""))
