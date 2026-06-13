from typing import Any


class StringUtils:
    @staticmethod
    def join(items: list[Any], separator: str) -> str:
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

    @staticmethod
    def splitAndClean(text: str, separator: str) -> list[str]:
        if not text:
            return []
        return [
            item.strip()
            for item in str(text).split(separator)
            if item.strip()
        ]
