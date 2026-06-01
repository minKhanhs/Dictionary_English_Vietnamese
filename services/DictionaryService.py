from algorithms.FuzzySearch import FuzzySearch
from config.AppConfig import AppConfig
from config.ResponseCode import ResponseCode
from models.FavoriteList import FavoriteList
from models.HistoryList import HistoryList
from models.Word import Word
from services.FileService import FileService
from structures.ArrayList import ArrayList
from structures.Trie import TrieNode
from utils.StringUtils import StringUtils
from validate.Validation import Validation


class DictionaryService:
    """CRUD từ điển, tìm kiếm, lịch sử, yêu thích."""

    def __init__(self, fileService=None):
        self.trieRoot = TrieNode()
        self.fuzzySearch = None
        self.words = ArrayList()
        self.history = HistoryList()
        self.favorites = FavoriteList()
        self.fileService = fileService or FileService()

    def loadData(self):
        """Tải dữ liệu từ file vào bộ nhớ."""
        try:
            self.trieRoot = TrieNode()
            self.words = ArrayList()
            self.history.clear()
            self.favorites.clear()
            for word in self.fileService.loadDictionary():
                self.words.add(word)
                self.trieRoot.insert(word.getEnglish())
            for item in self.fileService.loadHistory():
                self.history.add(item)
            for item in self.fileService.loadFavorites():
                self.favorites.add(item)
            self.fuzzySearch = FuzzySearch(self.trieRoot)
            print(f"{ResponseCode.PASS_LABEL} loadData")
        except Exception as e:
            print(f"{ResponseCode.FAIL_LABEL} loadData: {e}")

    def saveData(self):
        try:
            wordList = self._wordsToList()
            d = self.fileService.saveDictionary(wordList)
            h = self.fileService.saveHistory(self.history)
            f = self.fileService.saveFavorites(self.favorites)
            success = d and h and f
            if success:
                print(f"{ResponseCode.PASS_LABEL} saveData")
            else:
                print(f"{ResponseCode.FAIL_LABEL} saveData: một hoặc nhiều file ghi thất bại")
            return success
        except Exception as e:
            print(f"{ResponseCode.FAIL_LABEL} saveData: {e}")
            return False

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
        self.trieRoot.insert(word.getEnglish())
        return True

    def addWordInteractive(self):
        english = input("Từ tiếng Anh: ")
        vietnamese = input("Nghĩa tiếng Việt: ")
        example = input("Ví dụ (có thể để trống): ")
        synonymsInput = input("Từ đồng nghĩa (cách nhau bởi dấu phẩy, có thể để trống): ")
        synonyms = []
        if synonymsInput and synonymsInput.strip():
            synonyms = [
                item.strip()
                for item in synonymsInput.split(AppConfig.LIST_SEPARATOR)
                if item.strip()
            ]
        word = Word(english, vietnamese, example, synonyms)
        if self.addWordObject(word):
            print("Đã thêm từ thành công.")
            return True
        print("Không thể thêm từ. Kiểm tra lại dữ liệu hoặc từ đã tồn tại.")
        return False

    # --- READ ---

    def wordExists(self, word):
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return False
        return self.trieRoot.search(normalized)

    def searchExact(self, word):
        """Tìm chính xác. Tìm thấy → thêm vào history."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return None
        if not self.trieRoot.search(normalized):
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
            self.fuzzySearch = FuzzySearch(self.trieRoot)
        matchedWords = []
        for suggestion in self.fuzzySearch.getSuggestions(normalized):
            found = self._findWord(suggestion)
            if found is not None:
                matchedWords.append(found)
        return matchedWords

    def searchExactInteractive(self):
        english = input("Từ tiếng Anh: ")
        word = self.searchExact(english)
        if word is not None:
            word.display()
            return word
        print("Không tìm thấy từ.")
        self._displaySuggestions(english)
        return None

    def searchApproximateInteractive(self):
        english = input("Từ tiếng Anh: ")
        return self._displaySuggestions(english)

    # --- UPDATE ---

    def addSynonymInteractive(self):
        english = input("Từ tiếng Anh: ")
        word = self.searchExact(english)
        if word is None:
            print("Không tìm thấy từ.")
            return False
        synonym = input("Từ đồng nghĩa: ")
        if word.addSynonym(synonym):
            print("Đã thêm từ đồng nghĩa.")
            return True
        print("Không thể thêm từ đồng nghĩa (trùng hoặc không hợp lệ).")
        return False

    # --- DELETE ---

    def deleteWord(self, english):
        """Xóa từ. Rebuild Trie vì TrieNode không hỗ trợ delete."""
        normalized = StringUtils.normalizeWord(english) if english else ""
        if not normalized:
            return False
        found = False
        for i in range(self.words.size()):
            w = self.words.get(i)
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

    def deleteWordInteractive(self):
        english = input("Từ tiếng Anh cần xóa: ")
        normalized = StringUtils.normalizeWord(english) if english else ""
        if not self.wordExists(normalized):
            print("Không tìm thấy từ.")
            return False
        word = self._findWord(normalized)
        if word:
            print("Từ sẽ bị xóa:")
            word.display()
        confirm = input("Bạn có chắc muốn xóa? (y/n): ")
        if confirm.strip().lower() != "y":
            print("Đã hủy xóa.")
            return False
        if self.deleteWord(normalized):
            print("Đã xóa từ thành công.")
            return True
        print("Không thể xóa từ.")
        return False

    # --- HISTORY / FAVORITES / DISPLAY ---

    def showHistory(self):
        self.history.display()

    def addFavoriteInteractive(self):
        english = input("Từ tiếng Anh: ")
        normalized = StringUtils.normalizeWord(english) if english else ""
        if not self.wordExists(normalized):
            print("Từ phải tồn tại trong từ điển trước khi thêm vào yêu thích.")
            return False
        if self.favorites.add(normalized):
            print("Đã thêm vào yêu thích.")
            return True
        print("Từ đã có trong danh sách yêu thích.")
        return False

    def removeFavoriteInteractive(self):
        english = input("Từ tiếng Anh: ")
        if self.favorites.remove(english):
            print("Đã xóa khỏi yêu thích.")
            return True
        print("Không tìm thấy từ trong danh sách yêu thích.")
        return False

    def showFavorites(self):
        self.favorites.display()

    def displayAllWords(self):
        if self.words.size() == 0:
            print("Từ điển trống.")
            return
        for i in range(self.words.size()):
            print(f"\n{i + 1}.")
            self.words.get(i).display()

    # --- Internal ---

    def _findWord(self, english):
        normalized = StringUtils.normalizeWord(english) if english else ""
        for i in range(self.words.size()):
            w = self.words.get(i)
            if w.getEnglish() == normalized:
                return w
        return None

    def _rebuildTrie(self):
        self.trieRoot = TrieNode()
        for i in range(self.words.size()):
            w = self.words.get(i)
            self.trieRoot.insert(w.getEnglish())
        self.fuzzySearch = FuzzySearch(self.trieRoot)

    def _wordsToList(self):
        result = []
        for i in range(self.words.size()):
            result.append(self.words.get(i))
        return result

    def _displaySuggestions(self, english):
        suggestions = self.searchApproximate(english)
        if not suggestions:
            print("Không có gợi ý.")
            return []
        print("Gợi ý:")
        for index, word in enumerate(suggestions, start=1):
            print(f"{index}. {word.getEnglish()} - {word.getVietnamese()}")
        return suggestions
