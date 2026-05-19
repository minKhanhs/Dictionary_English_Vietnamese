from models.word import Word
from structures.trie import Trie


class TrieTest:
    @staticmethod
    def run(runner):
        trie = Trie()
        word = Word("hello", "xin chao")
        trie.insert(word)
        runner.assert_equal(word, trie.search("hello"), "trie finds inserted word")
        runner.assert_equal(None, trie.search("missing"), "trie returns None when missing")
        runner.assert_true(trie.starts_with("he"), "trie detects prefix")
        runner.assert_false(trie.starts_with("xy"), "trie rejects missing prefix")
