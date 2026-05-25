import unittest

from models.word import Word
from structures.trie import Trie


class TrieTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra cấu trúc Trie cho tra cứu chính xác và prefix
    """
    def test_trie_finds_inserted_word(self):
        # Sau khi insert, Trie phải tìm lại được đúng object Word đã thêm
        trie = Trie()
        word = Word("hello", "xin chao")

        trie.insert(word)

        self.assertEqual(word, trie.search("hello"))

    def test_trie_returns_none_when_word_is_missing(self):
        # Từ chưa insert phải trả về None
        trie = Trie()

        self.assertIsNone(trie.search("missing"))

    def test_trie_detects_existing_prefix(self):
        # Prefix "he" tồn tại vì đã có từ "hello"
        trie = Trie()
        trie.insert(Word("hello", "xin chao"))

        self.assertTrue(trie.starts_with("he"))

    def test_trie_rejects_missing_prefix(self):
        # Prefix "xy" không tồn tại trong Trie
        trie = Trie()
        trie.insert(Word("hello", "xin chao"))

        self.assertFalse(trie.starts_with("xy"))
