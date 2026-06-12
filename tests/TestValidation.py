import unittest

from config.AppConfig import AppConfig
from validate.Validation import Validation


class TestValidation(unittest.TestCase):
    """Kiểm tra Validation (các hàm kiểm tra đầu vào)."""

    def testIsEmptyNone(self):
        self.assertTrue(Validation.isEmpty(None))

    def testIsEmptyString(self):
        self.assertTrue(Validation.isEmpty(""))
        self.assertTrue(Validation.isEmpty("   "))

    def testIsNotEmpty(self):
        self.assertFalse(Validation.isEmpty("hello"))

    def testLengthValidInRange(self):
        self.assertTrue(Validation.isLengthValid("hello", 1, 10))

    def testLengthValidAtBounds(self):
        self.assertTrue(Validation.isLengthValid("a", 1, 10))
        self.assertTrue(Validation.isLengthValid("abcdefghij", 1, 10))

    def testLengthValidOutOfRange(self):
        self.assertFalse(Validation.isLengthValid("", 1, 10))
        self.assertFalse(Validation.isLengthValid("abcdefghijk", 1, 10))

    def testLengthValidNone(self):
        self.assertFalse(Validation.isLengthValid(None, 1, 10))

    def testEnglishWordValid(self):
        self.assertTrue(Validation.isEnglishWord("hello"))
        self.assertTrue(Validation.isEnglishWord("hello-world"))
        self.assertTrue(Validation.isEnglishWord("hello world"))
        self.assertTrue(Validation.isEnglishWord("HELLO"))

    def testEnglishWordWithNumbers(self):
        self.assertFalse(Validation.isEnglishWord("hello123"))

    def testEnglishWordWithSpecialChars(self):
        self.assertFalse(Validation.isEnglishWord("hello@world"))

    def testEnglishWordEmpty(self):
        self.assertFalse(Validation.isEnglishWord(""))
        self.assertFalse(Validation.isEnglishWord(None))

    def testVietnameseValid(self):
        self.assertTrue(Validation.isVietnameseMeaning("Xin chào"))

    def testVietnameseEmpty(self):
        self.assertFalse(Validation.isVietnameseMeaning(""))
        self.assertFalse(Validation.isVietnameseMeaning(None))

    def testExampleValid(self):
        self.assertTrue(Validation.isValidExample("Hello, how are you?"))

    def testExampleEmptyAllowed(self):
        self.assertTrue(Validation.isValidExample(""))
        self.assertTrue(Validation.isValidExample(None))

    def testSynonymValid(self):
        self.assertTrue(Validation.isValidSynonym("hi"))
        self.assertFalse(Validation.isValidSynonym("hi123"))

    def testMenuOptionValid(self):
        self.assertTrue(Validation.isValidMenuOption("0"))
        self.assertTrue(Validation.isValidMenuOption("5"))
        self.assertTrue(Validation.isValidMenuOption("11"))

    def testMenuOptionOutOfRange(self):
        self.assertFalse(Validation.isValidMenuOption("-1"))
        self.assertFalse(Validation.isValidMenuOption("12"))

    def testMenuOptionNonNumber(self):
        self.assertFalse(Validation.isValidMenuOption("abc"))
        self.assertFalse(Validation.isValidMenuOption(""))
        self.assertFalse(Validation.isValidMenuOption(None))

    def testHasEnoughFieldsValid(self):
        line = "hello|xin chào|example|hi,hey"
        self.assertTrue(Validation.hasEnoughFields(line, AppConfig.FIELD_SEPARATOR, 4))

    def testHasEnoughFieldsShort(self):
        self.assertFalse(
            Validation.hasEnoughFields("hello|xin chào", AppConfig.FIELD_SEPARATOR, 4)
        )

    def testHasEnoughFieldsEmpty(self):
        self.assertFalse(Validation.hasEnoughFields("", AppConfig.FIELD_SEPARATOR, 4))
        self.assertFalse(Validation.hasEnoughFields(None, AppConfig.FIELD_SEPARATOR, 4))

    def testValidDictionaryEntry(self):
        self.assertTrue(
            Validation.isValidDictionaryEntry("hello|Xin chào|Hello!|hi,hey")
        )
        self.assertTrue(Validation.isValidDictionaryEntry("hello|Xin chào|Hello!|"))

    def testInvalidDictionaryEntry(self):
        self.assertFalse(Validation.isValidDictionaryEntry("hello|Xin chào"))
        self.assertFalse(Validation.isValidDictionaryEntry("hello123|Xin chào|Hello!|"))
        self.assertFalse(Validation.isValidDictionaryEntry("hello||Hello!|"))


if __name__ == "__main__":
    unittest.main()
