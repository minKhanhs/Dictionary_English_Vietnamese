from config.AppConfig import AppConfig
from config.ResponseCode import ResponseCode
from structures.Word import Word


class MenuHandler:
    """Xử lý các thao tác từ người dùng, tách biệt khỏi logic hiển thị Menu."""

    def __init__(self, dictionaryService):
        self.dictionaryService = dictionaryService

    def addWord(self):
        english = input("Từ tiếng Anh: ")
        vietnamese = input("Nghĩa tiếng Việt: ")
        example = input("Ví dụ (có thể để trống): ")
        synonymsInput = input(
            "Từ đồng nghĩa (cách nhau bởi dấu phẩy, có thể để trống): "
        )
        synonyms = []
        if synonymsInput and synonymsInput.strip():
            synonyms = [
                item.strip()
                for item in synonymsInput.split(AppConfig.LIST_SEPARATOR)
                if item.strip()
            ]
        word = Word(english, vietnamese, example, synonyms)
        if self.dictionaryService.addWordObject(word):
            print(f"[{ResponseCode.SUCCESS}] Đã thêm từ thành công.")
        else:
            print(f"[{ResponseCode.ERROR}] Không thể thêm từ. Kiểm tra lại dữ liệu hoặc từ đã tồn tại.")

    def addSynonym(self):
        english = input("Từ tiếng Anh: ")
        word = self.dictionaryService.searchExact(english)
        if word is None:
            print(f"[{ResponseCode.NOT_FOUND}] Không tìm thấy từ.")
            return
        synonym = input("Từ đồng nghĩa: ")
        if word.addSynonym(synonym):
            print(f"[{ResponseCode.SUCCESS}] Đã thêm từ đồng nghĩa.")
        else:
            print(f"[{ResponseCode.ERROR}] Không thể thêm từ đồng nghĩa (trùng hoặc không hợp lệ).")

    def searchExact(self):
        english = input("Từ tiếng Anh: ")
        word = self.dictionaryService.searchExact(english)
        if word is not None:
            word.display()
        else:
            print(f"[{ResponseCode.NOT_FOUND}] Không tìm thấy từ.")
            self.displaySuggestions(english)

    def searchApproximate(self):
        english = input("Từ tiếng Anh: ")
        self.displaySuggestions(english)

    def displaySuggestions(self, english):
        suggestions = self.dictionaryService.searchApproximate(english)
        if not suggestions:
            print(f"[{ResponseCode.NOT_FOUND}] Không có gợi ý.")
            return
        print(f"[{ResponseCode.INFO}] Gợi ý:")
        for index, word in enumerate(suggestions, start=1):
            print(f"{index}. {word.getEnglish()} - {word.getVietnamese()}")

    def showHistory(self):
        self.dictionaryService.getHistory().display()

    def addFavorite(self):
        english = input("Từ tiếng Anh: ")
        if not self.dictionaryService.wordExists(english):
            print(f"[{ResponseCode.NOT_FOUND}] Từ phải tồn tại trong từ điển trước khi thêm vào yêu thích.")
            return
        if self.dictionaryService.getFavorites().add(english):
            print(f"[{ResponseCode.SUCCESS}] Đã thêm vào yêu thích.")
        else:
            print(f"[{ResponseCode.DUPLICATE}] Từ đã có trong danh sách yêu thích.")

    def removeFavorite(self):
        english = input("Từ tiếng Anh: ")
        if self.dictionaryService.getFavorites().remove(english):
            print(f"[{ResponseCode.SUCCESS}] Đã xóa khỏi yêu thích.")
        else:
            print(f"[{ResponseCode.NOT_FOUND}] Không tìm thấy từ trong danh sách yêu thích.")

    def showFavorites(self):
        self.dictionaryService.getFavorites().display()

    def displayAllWords(self):
        words = self.dictionaryService.getAllWords()
        if not words:
            print(f"[{ResponseCode.EMPTY}] Từ điển trống.")
            return
        for i, word in enumerate(words):
            print(f"\n{i + 1}.")
            if word is not None:
                word.display()

    def deleteWord(self):
        english = input("Từ tiếng Anh cần xóa: ")
        if not self.dictionaryService.wordExists(english):
            print(f"[{ResponseCode.NOT_FOUND}] Không tìm thấy từ.")
            return
        word = self.dictionaryService.getWord(english)
        if word:
            print(f"[{ResponseCode.INFO}] Từ sẽ bị xóa:")
            word.display()
        confirm = input("Bạn có chắc muốn xóa? (y/n): ")
        if confirm.strip().lower() != "y":
            print(f"[{ResponseCode.CANCELLED}] Đã hủy xóa.")
            return
        if self.dictionaryService.deleteWord(english):
            print(f"[{ResponseCode.SUCCESS}] Đã xóa từ thành công.")
        else:
            print(f"[{ResponseCode.ERROR}] Không thể xóa từ.")