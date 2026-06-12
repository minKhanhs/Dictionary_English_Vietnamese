from algorithms.FuzzySearch import FuzzySearch
from models.FavoriteList import FavoriteList
from models.HistoryList import HistoryList
from services.FileService import FileService
from structures.ArrayList import ArrayList
from structures.Trie import Trie
from structures.Word import Word
from utils.StringUtils import StringUtils
from validate.Validation import Validation


class DictionaryService:
    """CRUD từ điển, tìm kiếm, lịch sử, yêu thích."""

    def __init__(self, fileService=None):
        self.trie = Trie()
        self.fuzzySearch = None
        self.words = ArrayList()
        self.history = HistoryList()
        self.favorites = FavoriteList()
        self.fileService = fileService or FileService()

    def loadData(self):
        self.trie = Trie()
        self.words = ArrayList()
        self.history.clear()
        self.favorites.clear()
        for word in self.fileService.loadDictionary():
            self.importWordObject(word)
        for item in self.fileService.loadHistory():
            self.history.add(item)
        for item in self.fileService.loadFavorites():
            self.favorites.add(item)
        self.fuzzySearch = FuzzySearch(self.trie.root)

    def saveData(self):
        wordList = self.getAllWords()
        d = self.fileService.saveDictionary(wordList)
        h = self.fileService.saveHistory(self.history)
        f = self.fileService.saveFavorites(self.favorites)
        return d and h and f

    # --- CREATE ---

    def addWordObject(self, word):
        """Thêm Word object vào từ điển. Validate + kiểm tra trùng."""
        if word is None:
            return False
        if not Validation.isEnglishWord(word.getEnglish()):
            return False
        if not Validation.isVietnameseMeaning(word.getVietnamese()):
            return False
        if not Validation.isValidExample(word.getExample()):
            return False
        if self.wordExists(word.getEnglish()):
            return False
        self.words.add(word)
        self.trie.insert(word.getEnglish(), word)
        return True

    def importWordObject(self, word):
        """Import Word object. Từ trùng english sẽ được merge nghĩa/synonyms."""
        if word is None:
            return False
        if not Validation.isEnglishWord(word.getEnglish()):
            return False
        if not Validation.isVietnameseMeaning(word.getVietnamese()):
            return False
        if not Validation.isValidExample(word.getExample()):
            return False

        existing = self._findWord(word.getEnglish())
        if existing is None:
            self.words.add(word)
            self.trie.insert(word.getEnglish(), word)
            return True
        existing.mergeFrom(word)
        return True

    # --- READ ---

    def wordExists(self, word):
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return False
        return self.trie.search(normalized)

    def searchExact(self, word):
        """Tìm chính xác. Tìm thấy → thêm vào history."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return None
        if not self.trie.search(normalized):
            return None
        found = self._findWord(normalized)
        if found is not None:
            self.history.add(normalized)
        return found

    def searchApproximate(self, word):
        """Tìm gần đúng dùng FuzzySearch (Trie + Levenshtein đệ quy)."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return []
        if not self.fuzzySearch:
            self.fuzzySearch = FuzzySearch(self.trie.root)
        matchedWords = []
        for suggestion in self.fuzzySearch.getSuggestions(normalized):
            found = self._findWord(suggestion)
            if found is not None:
                matchedWords.append(found)
        return matchedWords

    def getWord(self, english):
        """Lấy Word object mà không ghi vào lịch sử (Dùng để hiển thị nội bộ)."""
        return self._findWord(english)

    # --- DELETE ---

    def deleteWord(self, english):
        """Xóa từ. Rebuild Trie vì TrieNode không hỗ trợ delete."""
        normalized = StringUtils.normalizeWord(english) if english else ""
        if not normalized:
            return False
        found = False
        for i in range(self.words.getSize()):
            w = self.words.get(i)
            if w is None:
                continue
            if w.getEnglish() == normalized:
                self.words.remove(i)
                found = True
                break
        if not found:
            return False
        self._rebuildTrie()
        if self.favorites.contains(normalized):
            self.favorites.remove(normalized)
        return True

    # --- HISTORY / FAVORITES / DISPLAY ---

    def getHistory(self):
        return self.history

    def getFavorites(self):
        return self.favorites

    def getAllWords(self):
        result = []
        for i in range(self.words.getSize()):
            result.append(self.words.get(i))
        return result

    # --- Internal ---

    def _findWord(self, english):
        normalized = StringUtils.normalizeWord(english) if english else ""
        if not normalized:
            return None
        return self.trie.searchData(normalized)

    def _rebuildTrie(self):
        self.trie = Trie()
        for i in range(self.words.getSize()):
            w = self.words.get(i)
            if w is None:
                continue
            self.trie.insert(w.getEnglish(), w)
        self.fuzzySearch = FuzzySearch(self.trie.root)
