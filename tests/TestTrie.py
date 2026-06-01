import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from structures.Trie import TrieNode


class TestTrie(unittest.TestCase):
    """Kiểm tra Trie insert, search, startsWith."""

    def setUp(self):
        self.trie = TrieNode()
        self.words = ["hello", "hell", "help", "helicopter", "hero", "cat", "car"]
        for word in self.words:
            self.trie.insert(word)

    def testSearchFound(self):
        self.assertTrue(self.trie.search("hello"))
        self.assertTrue(self.trie.search("cat"))

    def testSearchNotFound(self):
        self.assertFalse(self.trie.search("world"))
        self.assertFalse(self.trie.search("hel"))

    def testSearchEmpty(self):
        self.assertFalse(self.trie.search(""))

    def testInsertDuplicate(self):
        self.trie.insert("hello")
        self.assertTrue(self.trie.search("hello"))

    def testSearchCaseSensitive(self):
        self.assertFalse(self.trie.search("Hello"))

    def testStartsWithTrue(self):
        self.assertTrue(self.trie.startsWith("hel"))
        self.assertTrue(self.trie.startsWith("ca"))

    def testStartsWithFalse(self):
        self.assertFalse(self.trie.startsWith("xyz"))

    def testStartsWithEmpty(self):
        self.assertTrue(self.trie.startsWith(""))

    def testSingleChar(self):
        self.trie.insert("a")
        self.assertTrue(self.trie.search("a"))

    def testTrieEmpty(self):
        empty = TrieNode()
        self.assertFalse(empty.search("hello"))


if __name__ == "__main__":
    unittest.main()
