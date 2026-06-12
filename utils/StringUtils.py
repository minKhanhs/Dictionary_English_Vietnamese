class StringUtils:
    @staticmethod
    def join(items, separator):
        if not items:
            return ""
        return separator.join(str(item) for item in items)

    @staticmethod
    def normalizeWord(word: str) -> str:
        val = word.strip().lower()
        return StringUtils.removeExtraSpaces(val)

    @staticmethod
    def removeExtraSpaces(text: str) -> str:
        return " ".join(text.split())
