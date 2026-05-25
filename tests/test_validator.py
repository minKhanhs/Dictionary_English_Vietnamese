import unittest

from config.app_config import AppConfig
from validation.validator import Validator


class ValidatorTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra validation cho input, menu và dòng dữ liệu từ điển
    """
    def test_empty_spaces_are_detected(self):
        # Chuỗi chỉ có khoảng trắng phải được xem là rỗng
        self.assertTrue(Validator.is_empty("  "))

    def test_valid_english_word_allows_spaces(self):
        # Từ/cụm từ tiếng Anh hợp lệ có thể chứa khoảng trắng
        self.assertTrue(Validator.is_valid_english_word("ice cream"))

    def test_valid_english_word_allows_hyphen(self):
        # Từ ghép tiếng Anh hợp lệ có thể chứa dấu gạch nối
        self.assertTrue(Validator.is_valid_english_word("mother-in-law"))

    def test_valid_english_word_rejects_numbers(self):
        # Từ tiếng Anh chứa số phải bị từ chối
        self.assertFalse(Validator.is_valid_english_word("hello2"))

    def test_valid_english_word_rejects_empty_word(self):
        # Từ rỗng không phải input hợp lệ
        self.assertFalse(Validator.is_valid_english_word(""))

    def test_valid_vietnamese_meaning_accepts_text(self):
        # Nghĩa tiếng Việt không rỗng phải được chấp nhận
        self.assertTrue(Validator.is_valid_vietnamese_meaning("xin chao"))

    def test_menu_choice_accepts_max_option(self):
        # Lựa chọn menu bằng đúng MAX_MENU_OPTION vẫn hợp lệ
        self.assertTrue(
            Validator.is_valid_menu_choice(
                "10",
                AppConfig.MIN_MENU_OPTION,
                AppConfig.MAX_MENU_OPTION,
            )
        )

    def test_menu_choice_rejects_text(self):
        # Menu chỉ nhận số, nên chuỗi chữ phải bị từ chối
        self.assertFalse(Validator.is_valid_menu_choice("abc", 0, 10))

    def test_dictionary_line_is_accepted(self):
        # Dòng dữ liệu đủ trường theo định dạng word|meaning|example|synonyms phải hợp lệ
        self.assertTrue(Validator.is_valid_dictionary_line("hello|xin chao|Hello!|hi"))

    def test_short_dictionary_line_is_rejected(self):
        # Dòng thiếu trường phải bị từ chối
        self.assertFalse(Validator.is_valid_dictionary_line("hello|missing"))
