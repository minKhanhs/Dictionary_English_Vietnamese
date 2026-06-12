import unittest

from structures.Trie import Trie, TrieNode


class TestTrie(unittest.TestCase):
    """Kiểm tra Trie insert, search, startsWith."""

    def setUp(self):
        self.trie = TrieNode()
        self.wrapper = Trie()
        self.words = ["hello", "hell", "help", "helicopter", "hero", "cat", "car"]
        for word in self.words:
            self.trie.insert(word)
            self.wrapper.insert(word)

    def testSearchFound(self):
        self.assertTrue(self.trie.search("hello"))
        self.assertTrue(self.trie.search("cat"))
        self.assertTrue(self.wrapper.search("hello"))

    def testSearchNotFound(self):
        self.assertFalse(self.trie.search("world"))
        self.assertFalse(self.trie.search("hel"))
        self.assertFalse(self.wrapper.search("world"))

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
        self.assertTrue(self.wrapper.starts_with("hel"))

    def testStartsWithFalse(self):
        self.assertFalse(self.trie.startsWith("xyz"))
        self.assertFalse(self.wrapper.starts_with("xyz"))

    def testStartsWithEmpty(self):
        self.assertTrue(self.trie.startsWith(""))

    def testSingleChar(self):
        self.trie.insert("a")
        self.assertTrue(self.trie.search("a"))

    def testTrieEmpty(self):
        empty = TrieNode()
        self.assertFalse(empty.search("hello"))

    def testTrieRejectsInvalidCharacters(self):
        self.assertFalse(self.wrapper.insert("hello-world"))
        self.assertFalse(self.wrapper.search("hello-world"))
        self.assertFalse(self.wrapper.insert("hello world"))
        self.assertFalse(self.wrapper.search("hello world"))

    def testTrieStoresWordData(self):
        data = {"meaning": "xin chào"}
        self.assertTrue(self.wrapper.insert("hi", data))
        self.assertEqual(self.wrapper.search_data("hi"), data)

    def testTrieIndexHelpers(self):
        self.assertEqual(self.wrapper._get_index("a"), 0)
        self.assertEqual(self.wrapper._get_index("z"), 25)
        self.assertEqual(self.wrapper._get_index("-"), -1)
        self.assertTrue(self.wrapper._is_valid_char("a"))
        self.assertFalse(self.wrapper._is_valid_char("-"))


if __name__ == "__main__":
    unittest.main()
