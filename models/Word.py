# Model Word - Đại diện cho một mục từ trong từ điển Anh-Việt

from config.AppConfig import AppConfig
from utils.StringUtils import StringUtils
from validate.Validation import Validation


class Word:
    """Mục từ điển: từ tiếng Anh kèm nghĩa tiếng Việt, ví dụ, từ đồng nghĩa."""

    def __init__(self, english="", vietnamese="", example="", synonyms=None):
        self.english = StringUtils.normalizeWord(english) if english else ""
        self.vietnamese = str(vietnamese).strip() if vietnamese else ""
        self.example = str(example).strip() if example else ""
        self.synonyms = []
        if synonyms:
            for synonym in synonyms:
                self.add_synonym(synonym)

    # --- Getters ---

    def get_english(self):
        return self.english

    def get_vietnamese(self):
        return self.vietnamese

    def get_example(self):
        return self.example

    def get_synonyms(self):
        return list(self.synonyms)

    def get_synonym_count(self):
        return len(self.synonyms)

    # --- Setters ---

    def set_english(self, english):
        self.english = StringUtils.normalizeWord(english) if english else ""

    def set_vietnamese(self, vietnamese):
        self.vietnamese = str(vietnamese).strip() if vietnamese else ""

    def set_example(self, example):
        self.example = str(example).strip() if example else ""

    # --- Synonym management ---

    def add_synonym(self, synonym):
        """Thêm từ đồng nghĩa. Trả về True nếu thành công."""
        normalized = StringUtils.normalizeWord(synonym) if synonym else ""
        if not Validation.isEnglishWord(normalized):
            return False
        if self.has_synonym(normalized):
            return False
        if len(self.synonyms) >= AppConfig.MAX_SYNONYMS:
            return False
        self.synonyms.append(normalized)
        return True

    def has_synonym(self, synonym):
        """Kiểm tra từ đồng nghĩa đã tồn tại chưa."""
        normalized = StringUtils.normalizeWord(synonym) if synonym else ""
        return normalized in self.synonyms

    # --- Display & Serialization ---

    def display(self):
        """In thông tin từ ra console."""
        print("English:", self.english)
        print("Vietnamese:", self.vietnamese)
        if self.example:
            print("Example:", self.example)
        if self.synonyms:
            print("Synonyms:", StringUtils.join(self.synonyms, ", "))

    def to_file_line(self):
        """Chuyển thành dòng để ghi file. Dùng FIELD_SEPARATOR và LIST_SEPARATOR."""
        return AppConfig.FIELD_SEPARATOR.join([
            self.english,
            self.vietnamese,
            self.example,
            StringUtils.join(self.synonyms, AppConfig.LIST_SEPARATOR),
        ])

    @staticmethod
    def from_file_line(line):
        """Parse dòng file thành Word. Trả về None nếu dòng không hợp lệ."""
        if not line:
            return None
        if not Validation.isValidDictionaryEntry(str(line)):
            return None
        parts = str(line).rstrip("\n").split(AppConfig.FIELD_SEPARATOR)
        synonyms = []
        if len(parts) > 3 and parts[3].strip():
            synonyms = [
                item.strip()
                for item in parts[3].split(AppConfig.LIST_SEPARATOR)
                if item.strip()
            ]
        return Word(parts[0], parts[1], parts[2], synonyms)
