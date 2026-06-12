from config.AppConfig import AppConfig
from config.ResponseCode import ResponseCode
from utils.StringUtils import StringUtils
from validate.Validation import Validation


class Word:
    """Từ điển entry: english, vietnamese, example, synonyms."""

    def __init__(self, english="", vietnamese="", example="", synonyms=None):
        self.english = StringUtils.normalizeWord(english) if english else ""
        self.vietnamese = self._sanitize(vietnamese)
        self.example = self._sanitize(example)
        self.synonyms = []
        if synonyms:
            for synonym in synonyms:
                self.addSynonym(synonym)

    def getEnglish(self):
        return self.english

    def getVietnamese(self):
        return self.vietnamese

    def getExample(self):
        return self.example

    def getSynonyms(self):
        return list(self.synonyms)

    def getSynonymCount(self):
        return len(self.synonyms)

    def setEnglish(self, english):
        self.english = StringUtils.normalizeWord(english) if english else ""

    def setVietnamese(self, vietnamese):
        self.vietnamese = self._sanitize(vietnamese)

    def getMeaningList(self):
        return self._splitMeanings(self.vietnamese)

    def hasMeaning(self, meaning):
        normalized = self._normalizeMeaning(meaning)
        if not normalized:
            return False
        existing_meanings = (self._normalizeMeaning(item) for item in self.getMeaningList())
        return normalized in existing_meanings

    def addMeaning(self, meaning):
        clean = str(meaning).strip() if meaning else ""
        if not Validation.isVietnameseMeaning(clean):
            return False
        if self.hasMeaning(clean):
            return False
        meanings = self.getMeaningList()
        meanings.append(clean)
        self.vietnamese = f"{AppConfig.MEANING_SEPARATOR} ".join(meanings)
        return True

    def mergeFrom(self, other):
        if other is None or self.getEnglish() != other.getEnglish():
            return False
        changed = False
        for meaning in other.getMeaningList():
            if self.addMeaning(meaning):
                changed = True
        if not self.example and other.getExample():
            self.example = other.getExample()
            changed = True
        for synonym in other.getSynonyms():
            if self.addSynonym(synonym):
                changed = True
        return changed

    def setExample(self, example):
        self.example = self._sanitize(example)

    def addSynonym(self, synonym):
        """Thêm synonym. Không trùng, không vượt MAX_SYNONYMS."""
        normalized = StringUtils.normalizeWord(synonym) if synonym else ""
        if not Validation.isEnglishWord(normalized):
            return False
        if self.hasSynonym(normalized):
            return False
        if len(self.synonyms) >= AppConfig.MAX_SYNONYMS:
            return False
        self.synonyms.append(normalized)
        return True

    def hasSynonym(self, synonym):
        normalized = StringUtils.normalizeWord(synonym) if synonym else ""
        return normalized in self.synonyms

    @staticmethod
    def _normalizeMeaning(meaning):
        if not meaning:
            return ""
        return StringUtils.removeExtraSpaces(str(meaning).strip()).lower()

    @staticmethod
    def _splitMeanings(vietnamese):
        if not vietnamese:
            return []
        return [
            item.strip()
            for item in str(vietnamese).split(AppConfig.MEANING_SEPARATOR)
            if item.strip()
        ]

    @staticmethod
    def _sanitize(text):
        """Loại bỏ ký tự phân tách để tránh làm hỏng cấu trúc file lưu trữ."""
        if not text:
            return ""
        clean_text = str(text).replace(AppConfig.FIELD_SEPARATOR, " ")
        return clean_text.strip()

    def display(self):
        print(f"[{ResponseCode.INFO}] English: {self.english}")
        print(f"[{ResponseCode.INFO}] Vietnamese: {self.vietnamese}")
        if self.example:
            print(f"[{ResponseCode.INFO}] Example: {self.example}")
        if self.synonyms:
            syn_str = StringUtils.join(self.synonyms, ", ")
            print(f"[{ResponseCode.INFO}] Synonyms: {syn_str}")

    def toFileLine(self):
        return AppConfig.FIELD_SEPARATOR.join(
            [
                self.english,
                self.vietnamese,
                self.example,
                StringUtils.join(self.synonyms, AppConfig.LIST_SEPARATOR),
            ]
        )

    @staticmethod
    def fromFileLine(line):
        """Parse dòng file thành Word, None nếu không hợp lệ."""
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