# Service DictionaryService - Xử lý nghiệp vụ CRUD từ điển

from algorithms.Levenshtein import Levenshtein
from config.AppConfig import AppConfig
from models.FavoriteList import FavoriteList
from models.HistoryList import HistoryList
from models.Word import Word
from services.FileService import FileService
from structures.ArrayList import ArrayList
from structures.Trie import TrieNode
from utils.StringUtils import StringUtils
from validate.Validation import Validation


class DictionaryService:
    """Nghiệp vụ chính: CRUD từ điển, tìm kiếm, lịch sử, yêu thích."""

    def __init__(self, file_service=None):
        self.trie_root = TrieNode()
        self.words = ArrayList()
        self.history = HistoryList()
        self.favorites = FavoriteList()
        self.file_service = file_service or FileService()

    # --- Data loading / saving ---

    def load_data(self):
        """Tải dữ liệu từ file vào bộ nhớ."""
        self.trie_root = TrieNode()
        self.words = ArrayList()
        self.history.clear()
        self.favorites.clear()

        for word in self.file_service.load_dictionary():
            self.words.add(word)
            self.trie_root.insert(word.get_english())

        for item in self.file_service.load_history():
            self.history.add(item)
        for item in self.file_service.load_favorites():
            self.favorites.add(item)

    def save_data(self):
        """Lưu toàn bộ dữ liệu ra file."""
        word_list = self._words_to_list()
        d = self.file_service.save_dictionary(word_list)
        h = self.file_service.save_history(self.history)
        f = self.file_service.save_favorites(self.favorites)
        return d and h and f

    # --- CREATE ---

    def add_word_object(self, word):
        """Thêm Word object vào từ điển. Validate + kiểm tra trùng."""
        if word is None:
            return False
        if not Validation.isEnglishWord(word.get_english()):
            return False
        if not Validation.isVietnameseMeaning(word.get_vietnamese()):
            return False
        if not Validation.isValidExample(word.get_example()):
            return False
        if self.word_exists(word.get_english()):
            return False
        self.words.add(word)
        self.trie_root.insert(word.get_english())
        return True

    def add_word_interactive(self):
        """Thêm từ mới qua console input."""
        english = input("Từ tiếng Anh: ")
        vietnamese = input("Nghĩa tiếng Việt: ")
        example = input("Ví dụ (có thể để trống): ")
        synonyms_input = input("Từ đồng nghĩa (cách nhau bởi dấu phẩy, có thể để trống): ")
        synonyms = []
        if synonyms_input and synonyms_input.strip():
            synonyms = [
                item.strip()
                for item in synonyms_input.split(AppConfig.LIST_SEPARATOR)
                if item.strip()
            ]
        word = Word(english, vietnamese, example, synonyms)
        if self.add_word_object(word):
            print("Đã thêm từ thành công.")
            return True
        print("Không thể thêm từ. Kiểm tra lại dữ liệu hoặc từ đã tồn tại.")
        return False

    # --- READ ---

    def word_exists(self, word):
        """Kiểm tra từ tồn tại trong Trie."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return False
        return self.trie_root.search(normalized)

    def search_exact(self, word):
        """Tìm kiếm chính xác. Trả về Word object hoặc None.
        Nếu tìm thấy, tự động thêm vào lịch sử."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return None
        if not self.trie_root.search(normalized):
            return None
        # Tìm Word object trong ArrayList
        found = self._find_word(normalized)
        if found is not None:
            self.history.add(normalized)
        return found

    def search_approximate(self, word):
        """Tìm kiếm gần đúng dùng Levenshtein. Trả về danh sách Word."""
        normalized = StringUtils.normalizeWord(word) if word else ""
        if not normalized:
            return []
        lev = Levenshtein(normalized)
        # Xác định ngưỡng khoảng cách theo độ dài từ
        if len(normalized) <= AppConfig.SHORT_WORD_LENGTH:
            threshold = AppConfig.SHORT_WORD_DISTANCE
        elif len(normalized) <= AppConfig.MEDIUM_WORD_LENGTH:
            threshold = AppConfig.MEDIUM_WORD_DISTANCE
        else:
            threshold = AppConfig.LONG_WORD_DISTANCE
        suggestions = []
        for i in range(self.words.size()):
            w = self.words.get(i)
            distance = lev.distance(w.get_english())
            if distance <= threshold:
                suggestions.append((distance, w))
        suggestions.sort(key=lambda item: (item[0], item[1].get_english()))
        return [item[1] for item in suggestions[:AppConfig.MAX_SUGGESTIONS]]

    def search_exact_interactive(self):
        """Tìm kiếm chính xác qua console."""
        english = input("Từ tiếng Anh: ")
        word = self.search_exact(english)
        if word is not None:
            word.display()
            return word
        print("Không tìm thấy từ.")
        self._display_suggestions(english)
        return None

    def search_approximate_interactive(self):
        """Tìm kiếm gần đúng qua console."""
        english = input("Từ tiếng Anh: ")
        return self._display_suggestions(english)

    # --- UPDATE ---

    def add_synonym_interactive(self):
        """Thêm từ đồng nghĩa qua console."""
        english = input("Từ tiếng Anh: ")
        word = self.search_exact(english)
        if word is None:
            print("Không tìm thấy từ.")
            return False
        synonym = input("Từ đồng nghĩa: ")
        if word.add_synonym(synonym):
            print("Đã thêm từ đồng nghĩa.")
            return True
        print("Không thể thêm từ đồng nghĩa (trùng hoặc không hợp lệ).")
        return False

    # --- DELETE ---

    def delete_word(self, english):
        """Xóa từ khỏi từ điển. Trả về True nếu xóa thành công.
        Vì Trie hiện tại không hỗ trợ delete, rebuild Trie sau khi xóa."""
        normalized = StringUtils.normalizeWord(english) if english else ""
        if not normalized:
            return False
        # Tìm và xóa trong ArrayList
        found = False
        for i in range(self.words.size()):
            w = self.words.get(i)
            if w.get_english() == normalized:
                self.words.remove(i)
                found = True
                break
        if not found:
            return False
        # Rebuild Trie vì TrieNode không có phương thức delete
        self._rebuild_trie()
        # Xóa khỏi favorites nếu có
        if self.favorites.contains(normalized):
            self.favorites.remove(normalized)
        return True

    def delete_word_interactive(self):
        """Xóa từ qua console input."""
        english = input("Từ tiếng Anh cần xóa: ")
        normalized = StringUtils.normalizeWord(english) if english else ""
        if not self.word_exists(normalized):
            print("Không tìm thấy từ.")
            return False
        # Xác nhận trước khi xóa
        word = self._find_word(normalized)
        if word:
            print("Từ sẽ bị xóa:")
            word.display()
        confirm = input("Bạn có chắc muốn xóa? (y/n): ")
        if confirm.strip().lower() != "y":
            print("Đã hủy xóa.")
            return False
        if self.delete_word(normalized):
            print("Đã xóa từ thành công.")
            return True
        print("Không thể xóa từ.")
        return False

    # --- HISTORY ---

    def show_history(self):
        """Hiển thị lịch sử tra cứu."""
        self.history.display()

    # --- FAVORITES ---

    def add_favorite_interactive(self):
        """Thêm từ yêu thích qua console."""
        english = input("Từ tiếng Anh: ")
        normalized = StringUtils.normalizeWord(english) if english else ""
        if not self.word_exists(normalized):
            print("Từ phải tồn tại trong từ điển trước khi thêm vào yêu thích.")
            return False
        if self.favorites.add(normalized):
            print("Đã thêm vào yêu thích.")
            return True
        print("Từ đã có trong danh sách yêu thích.")
        return False

    def remove_favorite_interactive(self):
        """Xóa từ yêu thích qua console."""
        english = input("Từ tiếng Anh: ")
        if self.favorites.remove(english):
            print("Đã xóa khỏi yêu thích.")
            return True
        print("Không tìm thấy từ trong danh sách yêu thích.")
        return False

    def show_favorites(self):
        """Hiển thị danh sách yêu thích."""
        self.favorites.display()

    # --- DISPLAY ---

    def display_all_words(self):
        """Hiển thị tất cả từ trong từ điển."""
        if self.words.size() == 0:
            print("Từ điển trống.")
            return
        for i in range(self.words.size()):
            print(f"\n{i + 1}.")
            self.words.get(i).display()

    # --- Internal helpers ---

    def _find_word(self, english):
        """Tìm Word object trong ArrayList theo english."""
        normalized = StringUtils.normalizeWord(english) if english else ""
        for i in range(self.words.size()):
            w = self.words.get(i)
            if w.get_english() == normalized:
                return w
        return None

    def _rebuild_trie(self):
        """Rebuild Trie từ ArrayList (dùng sau khi xóa từ)."""
        self.trie_root = TrieNode()
        for i in range(self.words.size()):
            w = self.words.get(i)
            self.trie_root.insert(w.get_english())

    def _words_to_list(self):
        """Chuyển ArrayList thành list Python."""
        result = []
        for i in range(self.words.size()):
            result.append(self.words.get(i))
        return result

    def _display_suggestions(self, english):
        """Hiển thị gợi ý tìm kiếm gần đúng."""
        suggestions = self.search_approximate(english)
        if not suggestions:
            print("Không có gợi ý.")
            return []
        print("Gợi ý:")
        for index, word in enumerate(suggestions, start=1):
            print(f"{index}. {word.get_english()} - {word.get_vietnamese()}")
        return suggestions
