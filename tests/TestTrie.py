# Test Trie - Kiểm tra cấu trúc dữ liệu Trie

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from structures.Trie import TrieNode


class TestTrie(unittest.TestCase):
    """Test Suite: Kiểm tra Trie insert, search, startsWith"""

    def setUp(self):
        self.trie = TrieNode()
        self.words = ["hello", "hell", "help", "helicopter", "hero", "cat", "car"]
        for word in self.words:
            self.trie.insert(word)

    # --- Insert & Search ---

    def test_search_found(self):
        """Tìm thấy từ đã insert"""
        self.assertTrue(self.trie.search("hello"))
        self.assertTrue(self.trie.search("cat"))
        self.assertTrue(self.trie.search("car"))

    def test_search_not_found(self):
        """Không tìm thấy từ chưa insert"""
        self.assertFalse(self.trie.search("world"))
        self.assertFalse(self.trie.search("hel"))
        self.assertFalse(self.trie.search("xyz"))

    def test_search_empty_string(self):
        """Chuỗi rỗng không crash"""
        # Trie.search với chuỗi rỗng trả về isEndOfWord của root = False
        self.assertFalse(self.trie.search(""))

    def test_insert_duplicate(self):
        """Insert từ trùng không gây lỗi"""
        self.trie.insert("hello")
        self.assertTrue(self.trie.search("hello"))

    def test_search_case_sensitive(self):
        """Trie hiện tại phân biệt hoa thường (insert lowercase)"""
        # "hello" đã insert, nhưng "Hello" có chữ H hoa → không tìm thấy
        self.assertFalse(self.trie.search("Hello"))

    # --- StartsWith ---

    def test_starts_with_true(self):
        """Prefix tồn tại"""
        self.assertTrue(self.trie.startsWith("hel"))
        self.assertTrue(self.trie.startsWith("ca"))
        self.assertTrue(self.trie.startsWith("h"))

    def test_starts_with_false(self):
        """Prefix không tồn tại"""
        self.assertFalse(self.trie.startsWith("xyz"))
        self.assertFalse(self.trie.startsWith("abc"))

    def test_starts_with_empty(self):
        """Prefix rỗng luôn trả về True (duyệt hết root)"""
        self.assertTrue(self.trie.startsWith(""))

    # --- Edge cases ---

    def test_single_char_word(self):
        """Từ 1 ký tự"""
        self.trie.insert("a")
        self.assertTrue(self.trie.search("a"))
        self.assertTrue(self.trie.startsWith("a"))

    def test_trie_empty(self):
        """Trie rỗng"""
        empty_trie = TrieNode()
        self.assertFalse(empty_trie.search("hello"))
        self.assertFalse(empty_trie.startsWith("h"))


if __name__ == "__main__":
    unittest.main()
