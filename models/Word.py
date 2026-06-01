from config.AppConfig import AppConfig
from utils.StringUtils import StringUtils
from validate.Validation import Validation


class Word:
    """Từ điển entry: english, vietnamese, example, synonyms."""

    def __init__(self, english="", vietnamese="", example="", synonyms=None):
        self.english = StringUtils.normalizeWord(english) if english else ""
        self.vietnamese = str(vietnamese).strip() if vietnamese else ""
        self.example = str(example).strip() if example else ""
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
        self.vietnamese = str(vietnamese).strip() if vietnamese else ""

    def setExample(self, example):
        self.example = str(example).strip() if example else ""

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

    def display(self):
        print("English:", self.english)
        print("Vietnamese:", self.vietnamese)
        if self.example:
            print("Example:", self.example)
        if self.synonyms:
            print("Synonyms:", StringUtils.join(self.synonyms, ", "))

    def toFileLine(self):
        return AppConfig.FIELD_SEPARATOR.join([
            self.english,
            self.vietnamese,
            self.example,
            StringUtils.join(self.synonyms, AppConfig.LIST_SEPARATOR),
        ])

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
