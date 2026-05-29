# Test Validation - Kiểm tra các hàm validation đầu vào

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.AppConfig import AppConfig
from validate.Validation import Validation


class TestValidation(unittest.TestCase):
    """Test Suite: Kiểm tra Validation (các hàm kiểm tra đầu vào)"""

    # --- isEmpty ---

    def test_is_empty_none(self):
        self.assertTrue(Validation.isEmpty(None))

    def test_is_empty_string(self):
        self.assertTrue(Validation.isEmpty(""))

    def test_is_empty_whitespace(self):
        self.assertTrue(Validation.isEmpty("   "))

    def test_is_empty_not_empty(self):
        self.assertFalse(Validation.isEmpty("hello"))

    # --- isLengthValid ---

    def test_length_valid_in_range(self):
        self.assertTrue(Validation.isLengthValid("hello", 1, 10))

    def test_length_valid_at_min(self):
        self.assertTrue(Validation.isLengthValid("a", 1, 10))

    def test_length_valid_at_max(self):
        self.assertTrue(Validation.isLengthValid("abcdefghij", 1, 10))

    def test_length_valid_below_min(self):
        self.assertFalse(Validation.isLengthValid("", 1, 10))

    def test_length_valid_above_max(self):
        self.assertFalse(Validation.isLengthValid("abcdefghijk", 1, 10))

    def test_length_valid_none(self):
        self.assertFalse(Validation.isLengthValid(None, 1, 10))

    # --- isEnglishWord ---

    def test_english_word_valid(self):
        self.assertTrue(Validation.isEnglishWord("hello"))
        self.assertTrue(Validation.isEnglishWord("hello-world"))
        self.assertTrue(Validation.isEnglishWord("hello world"))

    def test_english_word_uppercase(self):
        """Hoa thường vẫn hợp lệ (normalize bên trong)"""
        self.assertTrue(Validation.isEnglishWord("HELLO"))

    def test_english_word_with_numbers(self):
        """Không chấp nhận số"""
        self.assertFalse(Validation.isEnglishWord("hello123"))

    def test_english_word_with_special_chars(self):
        """Không chấp nhận ký tự đặc biệt"""
        self.assertFalse(Validation.isEnglishWord("hello@world"))
        self.assertFalse(Validation.isEnglishWord("hello.world"))

    def test_english_word_empty(self):
        self.assertFalse(Validation.isEnglishWord(""))

    def test_english_word_none(self):
        self.assertFalse(Validation.isEnglishWord(None))

    # --- isVietnameseMeaning ---

    def test_vietnamese_valid(self):
        self.assertTrue(Validation.isVietnameseMeaning("Xin chào"))
        self.assertTrue(Validation.isVietnameseMeaning("học sinh"))

    def test_vietnamese_empty(self):
        self.assertFalse(Validation.isVietnameseMeaning(""))

    def test_vietnamese_none(self):
        self.assertFalse(Validation.isVietnameseMeaning(None))

    # --- isValidExample ---

    def test_example_valid(self):
        self.assertTrue(Validation.isValidExample("Hello, how are you?"))

    def test_example_empty_allowed(self):
        """Ví dụ có thể để trống"""
        self.assertTrue(Validation.isValidExample(""))

    def test_example_none(self):
        self.assertTrue(Validation.isValidExample(None))

    # --- isValidSynonym ---

    def test_synonym_valid(self):
        self.assertTrue(Validation.isValidSynonym("hi"))

    def test_synonym_invalid(self):
        self.assertFalse(Validation.isValidSynonym("hi123"))

    # --- isValidMenuOption ---

    def test_menu_option_valid(self):
        self.assertTrue(Validation.isValidMenuOption("0"))
        self.assertTrue(Validation.isValidMenuOption("5"))
        self.assertTrue(Validation.isValidMenuOption("11"))

    def test_menu_option_out_of_range(self):
        self.assertFalse(Validation.isValidMenuOption("-1"))
        self.assertFalse(Validation.isValidMenuOption("12"))

    def test_menu_option_non_number(self):
        self.assertFalse(Validation.isValidMenuOption("abc"))
        self.assertFalse(Validation.isValidMenuOption(""))

    def test_menu_option_none(self):
        self.assertFalse(Validation.isValidMenuOption(None))

    # --- hasEnoughFields ---

    def test_enough_fields_valid(self):
        line = "hello|xin chào|example|hi,hey"
        self.assertTrue(Validation.hasEnoughFields(line, AppConfig.FIELD_SEPARATOR, 4))

    def test_enough_fields_short(self):
        line = "hello|xin chào"
        self.assertFalse(Validation.hasEnoughFields(line, AppConfig.FIELD_SEPARATOR, 4))

    def test_enough_fields_empty(self):
        self.assertFalse(Validation.hasEnoughFields("", AppConfig.FIELD_SEPARATOR, 4))
        self.assertFalse(Validation.hasEnoughFields(None, AppConfig.FIELD_SEPARATOR, 4))

    # --- isValidDictionaryEntry ---

    def test_valid_entry(self):
        """Dòng file từ điển hợp lệ"""
        line = "hello|Xin chào|Hello!|hi,hey"
        self.assertTrue(Validation.isValidDictionaryEntry(line))

    def test_valid_entry_no_synonyms(self):
        """Dòng hợp lệ không có synonym (field 4 rỗng)"""
        line = "hello|Xin chào|Hello!|"
        self.assertTrue(Validation.isValidDictionaryEntry(line))

    def test_invalid_entry_missing_fields(self):
        """Thiếu field"""
        line = "hello|Xin chào"
        self.assertFalse(Validation.isValidDictionaryEntry(line))

    def test_invalid_entry_bad_english(self):
        """Từ tiếng Anh không hợp lệ (có số)"""
        line = "hello123|Xin chào|Hello!|"
        self.assertFalse(Validation.isValidDictionaryEntry(line))

    def test_invalid_entry_empty_meaning(self):
        """Nghĩa tiếng Việt rỗng"""
        line = "hello||Hello!|"
        self.assertFalse(Validation.isValidDictionaryEntry(line))


if __name__ == "__main__":
    unittest.main()
