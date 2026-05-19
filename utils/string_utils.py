class StringUtils:
    """Small helpers for defensive string handling."""

    @staticmethod
    def trim(value):
        if value is None:
            return ""
        return str(value).strip()

    @staticmethod
    def to_lower_case(value):
        return StringUtils.trim(value).lower()

    @staticmethod
    def remove_extra_spaces(value):
        return " ".join(StringUtils.trim(value).split())

    @staticmethod
    def normalize_word(value):
        return StringUtils.remove_extra_spaces(StringUtils.to_lower_case(value))

    @staticmethod
    def split(value, separator):
        if value is None:
            return []
        return str(value).split(separator)

    @staticmethod
    def join(items, separator):
        if not items:
            return ""
        return separator.join(str(item) for item in items)
