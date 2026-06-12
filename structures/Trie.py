from config.AppConfig import AppConfig


class TrieNode:
    """Node trong cây Trie."""

    def __init__(self):
        self.children = {}
        self.isEndOfWord = False
        self.wordData = None


class Trie:
    """Trie cho tra cứu chính xác từ tiếng Anh a-z."""

    def __init__(self, root=None):
        self.root = root or TrieNode()

    def insert(self, word, word_data=None):
        if not word or not self._isValidWord(word):
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
        if not english or not self._isValidWord(english):
            return False
        node = self.root
        for char in english:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.isEndOfWord

    def searchData(self, english):
        if not english or not self._isValidWord(english):
            return None
        node = self.root
        for char in english:
            if char not in node.children:
                return None
            node = node.children[char]
        if not node.isEndOfWord:
            return None
        return node.wordData

    def startsWith(self, prefix):
        if prefix is None or not self._isValidWord(prefix):
            return False
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def _getIndex(self, char):
        if not self._isValidChar(char):
            return -1
        return ord(char) - ord(AppConfig.FIRST_CHAR)

    def _isValidChar(self, char):
        return (
            isinstance(char, str)
            and len(char) == 1
            and AppConfig.FIRST_CHAR <= char <= AppConfig.LAST_CHAR
        )

    def _isValidWord(self, word):
        return isinstance(word, str) and all(self._isValidChar(char) for char in word)
