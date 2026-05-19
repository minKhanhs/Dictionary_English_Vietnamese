from config.app_config import AppConfig
from validation.validator import Validator


class ValidatorTest:
    @staticmethod
    def run(runner):
        runner.assert_true(Validator.is_empty("  "), "empty spaces detected")
        runner.assert_true(Validator.is_valid_english_word("ice cream"), "valid spaces")
        runner.assert_true(Validator.is_valid_english_word("mother-in-law"), "valid hyphen")
        runner.assert_false(Validator.is_valid_english_word("hello2"), "word with number rejected")
        runner.assert_false(Validator.is_valid_english_word(""), "empty word rejected")
        runner.assert_true(
            Validator.is_valid_vietnamese_meaning("xin chao"), "meaning accepted"
        )
        runner.assert_true(
            Validator.is_valid_menu_choice(
                "10", AppConfig.MIN_MENU_OPTION, AppConfig.MAX_MENU_OPTION
            ),
            "menu choice max accepted",
        )
        runner.assert_false(
            Validator.is_valid_menu_choice("abc", 0, 10), "menu text rejected"
        )
        runner.assert_true(
            Validator.is_valid_dictionary_line("hello|xin chao|Hello!|hi"),
            "dictionary line accepted",
        )
        runner.assert_false(
            Validator.is_valid_dictionary_line("hello|missing"),
            "short dictionary line rejected",
        )
