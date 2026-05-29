# Service FileService - Đọc/ghi dữ liệu từ file text

import os

from config.AppConfig import AppConfig
from models.Word import Word
from utils.StringUtils import StringUtils
from validate.Validation import Validation


class FileService:
    """Đọc và ghi dữ liệu từ điển, lịch sử, yêu thích ra file text."""

    def ensure_data_files(self):
        """Tạo file dữ liệu nếu chưa tồn tại."""
        folder = os.path.dirname(AppConfig.DICTIONARY_FILE)
        if folder:
            os.makedirs(folder, exist_ok=True)
        for path in (AppConfig.DICTIONARY_FILE, AppConfig.HISTORY_FILE, AppConfig.FAVORITES_FILE):
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8"):
                    pass

    def load_dictionary(self):
        """Đọc từ điển từ file. Bỏ qua dòng sai định dạng."""
        self.ensure_data_files()
        words = []
        try:
            with open(AppConfig.DICTIONARY_FILE, "r", encoding="utf-8") as file:
                for line in file:
                    word = Word.from_file_line(line)
                    if word is not None:
                        words.append(word)
        except OSError as error:
            print("Không thể đọc file từ điển:", error)
        return words

    def save_dictionary(self, words_list):
        """Ghi danh sách Word ra file. Trả về True nếu thành công."""
        self.ensure_data_files()
        try:
            with open(AppConfig.DICTIONARY_FILE, "w", encoding="utf-8") as file:
                for word in words_list:
                    file.write(word.to_file_line() + "\n")
            return True
        except OSError as error:
            print("Không thể ghi file từ điển:", error)
            return False

    def load_history(self):
        """Đọc lịch sử từ file."""
        return self._load_simple_file(AppConfig.HISTORY_FILE)

    def save_history(self, history_list):
        """Ghi lịch sử ra file. Nhận list hoặc đối tượng có to_list()."""
        return self._save_simple_file(AppConfig.HISTORY_FILE, history_list)

    def load_favorites(self):
        """Đọc danh sách yêu thích từ file."""
        return self._load_simple_file(AppConfig.FAVORITES_FILE)

    def save_favorites(self, favorites_list):
        """Ghi danh sách yêu thích ra file."""
        return self._save_simple_file(AppConfig.FAVORITES_FILE, favorites_list)

    # --- Internal helpers ---

    def _load_simple_file(self, path):
        """Đọc file đơn giản, mỗi dòng một từ."""
        self.ensure_data_files()
        items = []
        try:
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    normalized = StringUtils.normalizeWord(line)
                    if normalized:
                        items.append(normalized)
        except OSError as error:
            print("Không thể đọc file:", error)
        return items

    def _save_simple_file(self, path, values):
        """Ghi file đơn giản, mỗi dòng một từ."""
        self.ensure_data_files()
        items = values.to_list() if hasattr(values, "to_list") else values
        try:
            with open(path, "w", encoding="utf-8") as file:
                for item in items:
                    normalized = StringUtils.normalizeWord(item)
                    if normalized:
                        file.write(normalized + "\n")
            return True
        except OSError as error:
            print("Không thể ghi file:", error)
            return False
