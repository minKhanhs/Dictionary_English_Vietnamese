from utils.StringUtils import StringUtils
from config.AppConfig import AppConfig
class Validation:

    @staticmethod
    def isEmpty(val):
        return val is None or len(str(val).strip()) == 0
    
    @staticmethod
    def isLengthValid(val, min_length, max_length):
        if val is None:
            return False
        length = len(str(val))
        return min_length <= length <= max_length
    
    @staticmethod
    def isEnglishWord(val):
        if Validation.isEmpty(val):
            return False
        word = StringUtils.normalizeWord(str(val))
        if not Validation.isLengthValid(word, AppConfig.MIN_WORD_LENGTH, AppConfig.MAX_WORD_LENGTH):
            return False
        for char in word:
            if not (char.isalpha() or char in [' ', '-']):
                return False
        return True
    
    @staticmethod
    def isVietnameseMeaning(val):
        if Validation.isEmpty(val):
            return False
        meaning = str(val).strip()
        return Validation.isLengthValid(meaning, AppConfig.MIN_MEANING_LENGTH, AppConfig.MAX_MEANING_LENGTH)

    @staticmethod
    def isValidExample(val):
        if Validation.isEmpty(val):
            return True # Cho phép ví dụ trống
        example = str(val).strip()
        return Validation.isLengthValid(example, AppConfig.MIN_EXAMPLE_LENGTH, AppConfig.MAX_EXAMPLE_LENGTH) 

    @staticmethod
    def isValidSynonym(val):
        return Validation.isEnglishWord(val)
    
    @staticmethod
    def isValidMenuOption(val):
        if Validation.isEmpty(val):
            return False
        try:
            option = int(val)
            return AppConfig.MIN_MENU_OPTION <= option <= AppConfig.MAX_MENU_OPTION
        except (ValueError,TypeError):
            return False
    
    @staticmethod
    def hasEnoughFields(line, separator, expected_fields):
        if not line:
            return False
        parts = line.split(separator)
        return len(parts) >= expected_fields
    
    @staticmethod
    def isValidDictionaryEntry(line):
        if not Validation.hasEnoughFields(line, AppConfig.FIELD_SEPARATOR, AppConfig.DICTIONARY_FILE_FIELD_COUNT):
            return False
        parts = line.split(AppConfig.FIELD_SEPARATOR)
        return Validation.isEnglishWord(parts[0]) and not Validation.isEmpty(parts[1])