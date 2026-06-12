import unittest

from structures.Trie import Trie


class TestTrie(unittest.TestCase):
    """Kiểm tra Trie insert, search, startsWith."""

    def setUp(self):
        self.trie = Trie()
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
        empty = Trie()
        self.assertFalse(empty.search("hello"))

    def testTrieRejectsInvalidCharacters(self):
        self.assertFalse(self.trie.insert("hello-world"))
        self.assertFalse(self.trie.search("hello-world"))
        self.assertFalse(self.trie.insert("hello world"))
        self.assertFalse(self.trie.search("hello world"))

    def testTrieStoresWordData(self):
        data = {"meaning": "xin chào"}
        self.assertTrue(self.trie.insert("hi", data))
        self.assertEqual(self.trie.searchData("hi"), data)

    def testTrieIndexHelpers(self):
        self.assertEqual(self.trie._getIndex("a"), 0)
        self.assertEqual(self.trie._getIndex("z"), 25)
        self.assertEqual(self.trie._getIndex("-"), -1)
        self.assertTrue(self.trie._isValidChar("a"))
        self.assertFalse(self.trie._isValidChar("-"))


if __name__ == "__main__":
    unittest.main()
