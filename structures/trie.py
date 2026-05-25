from config.app_config import AppConfig
from utils.string_utils import StringUtils


class TrieNode:
    """Node used by Trie exact search."""

    def __init__(self):
        self.children = [None] * AppConfig.ALPHABET_SIZE
        self.is_end_of_word = False
        self.word_data = None


class Trie:
    """Trie for exact a-z word lookup."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        english = word.get_english() if hasattr(word, "get_english") else word
        normalized = StringUtils.normalize_word(english)
        node = self.root
        for char in normalized:
            if not self._is_valid_char(char):
                continue
            index = self._get_index(char)
            if node.children[index] is None:
                node.children[index] = TrieNode()
            node = node.children[index]
        node.is_end_of_word = True
        node.word_data = word

    def search(self, english):
        node = self._find_node(english)
        if node and node.is_end_of_word:
            return node.word_data
        return None

    def starts_with(self, prefix):
        return self._find_node(prefix) is not None

    def _find_node(self, value):
        normalized = StringUtils.normalize_word(value)
        node = self.root
        for char in normalized:
            if not self._is_valid_char(char):
                continue
            index = self._get_index(char)
            if node.children[index] is None:
                return None
            node = node.children[index]
        return node

    def _get_index(self, char):
        return ord(char) - ord(AppConfig.FIRST_CHAR)

    def _is_valid_char(self, char):
        return AppConfig.FIRST_CHAR <= char <= AppConfig.LAST_CHAR
