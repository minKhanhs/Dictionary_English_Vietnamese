from config.AppConfig import AppConfig


class TrieNode:
    """Node trong cây Trie."""

    def __init__(self):
        self.children = {}
        self.isEndOfWord = False
        self.wordData = None

    def insert(self, word):
        return Trie(self).insert(word)

    def search(self, word):
        return Trie(self).search(word)

    def startsWith(self, prefix):
        return Trie(self).starts_with(prefix)

    @property
    def is_end_of_word(self):
        return self.isEndOfWord

    @is_end_of_word.setter
    def is_end_of_word(self, value):
        self.isEndOfWord = value

    @property
    def word_data(self):
        return self.wordData

    @word_data.setter
    def word_data(self, value):
        self.wordData = value


class Trie:
    """Trie cho tra cứu chính xác từ tiếng Anh a-z."""

    def __init__(self, root=None):
        self.root = root or TrieNode()

    def insert(self, word, word_data=None):
        if not word or not self._is_valid_word(word):
            return False
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.isEndOfWord = True
        node.wordData = word_data
        return True

    def search(self, english):
        if not english or not self._is_valid_word(english):
            return False
        node = self.root
        for char in english:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.isEndOfWord

    def search_data(self, english):
        if not english or not self._is_valid_word(english):
            return None
        node = self.root
        for char in english:
            if char not in node.children:
                return None
            node = node.children[char]
        if not node.isEndOfWord:
            return None
        return node.wordData

    def starts_with(self, prefix):
        if prefix is None or not self._is_valid_word(prefix):
            return False
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def startsWith(self, prefix):
        return self.starts_with(prefix)

    def _get_index(self, char):
        if not self._is_valid_char(char):
            return -1
        return ord(char) - ord(AppConfig.FIRST_CHAR)

    def _is_valid_char(self, char):
        return (
            isinstance(char, str)
            and len(char) == 1
            and AppConfig.FIRST_CHAR <= char <= AppConfig.LAST_CHAR
        )

    def _is_valid_word(self, word):
        return isinstance(word, str) and all(self._is_valid_char(char) for char in word)
