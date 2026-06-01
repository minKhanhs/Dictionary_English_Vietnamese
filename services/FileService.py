import os

from config.AppConfig import AppConfig
from models.Word import Word
from utils.StringUtils import StringUtils


class FileService:
    """Đọc/ghi dữ liệu từ điển, lịch sử, yêu thích ra file text."""

    def ensureDataFiles(self):
        folder = os.path.dirname(AppConfig.DICTIONARY_FILE)
        if folder:
            os.makedirs(folder, exist_ok=True)
        for path in (AppConfig.DICTIONARY_FILE, AppConfig.HISTORY_FILE, AppConfig.FAVORITES_FILE):
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8"):
                    pass

    def loadDictionary(self):
        """Đọc từ điển từ file, bỏ qua dòng sai định dạng."""
        self.ensureDataFiles()
        words = []
        try:
            with open(AppConfig.DICTIONARY_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    word = Word.fromFileLine(line)
                    if word is not None:
                        words.append(word)
        except OSError as e:
            print("Không thể đọc file từ điển:", e)
        return words

    def saveDictionary(self, wordsList):
        self.ensureDataFiles()
        try:
            with open(AppConfig.DICTIONARY_FILE, "w", encoding="utf-8") as f:
                for word in wordsList:
                    f.write(word.toFileLine() + "\n")
            return True
        except OSError as e:
            print("Không thể ghi file từ điển:", e)
            return False

    def loadHistory(self):
        return self._loadSimpleFile(AppConfig.HISTORY_FILE)

    def saveHistory(self, historyObj):
        return self._saveSimpleFile(AppConfig.HISTORY_FILE, historyObj)

    def loadFavorites(self):
        return self._loadSimpleFile(AppConfig.FAVORITES_FILE)

    def saveFavorites(self, favoritesObj):
        return self._saveSimpleFile(AppConfig.FAVORITES_FILE, favoritesObj)

    def _loadSimpleFile(self, path):
        self.ensureDataFiles()
        items = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    normalized = StringUtils.normalizeWord(line)
                    if normalized:
                        items.append(normalized)
        except OSError as e:
            print("Không thể đọc file:", e)
        return items

    def _saveSimpleFile(self, path, values):
        self.ensureDataFiles()
        items = values.toList() if hasattr(values, "toList") else values
        try:
            with open(path, "w", encoding="utf-8") as f:
                for item in items:
                    normalized = StringUtils.normalizeWord(item)
                    if normalized:
                        f.write(normalized + "\n")
            return True
        except OSError as e:
            print("Không thể ghi file:", e)
            return False
