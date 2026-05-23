import unittest

from config.app_config import AppConfig
from models.word import Word


class WordTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra model Word, synonym và chuyển đổi dữ liệu file
    """
    def test_word_normalizes_english(self):
        # Từ tiếng Anh phải được chuẩn hóa: bỏ khoảng trắng và chuyển về chữ thường
        word = Word(" Hello ", "xin chao", "Hello!", ["hi"])

        self.assertEqual("hello", word.get_english())

    def test_add_synonym_rejects_duplicates(self):
        # Thêm synonym mới thành công, nhưng synonym trùng phải bị từ chối
        word = Word("hello", "xin chao", "Hello!", ["hi"])

        self.assertTrue(word.add_synonym("hey"))
        self.assertFalse(word.add_synonym("hey"))
        self.assertEqual(2, word.get_synonym_count())

    def test_word_round_trip_from_file_line(self):
        # Dữ liệu Word ghi ra file rồi đọc lại phải giữ nguyên các trường chính
        word = Word(" Hello ", "xin chao", "Hello!", ["hi"])

        parsed = Word.from_file_line(word.to_file_line())

        self.assertEqual("hello", parsed.get_english())
        self.assertEqual("xin chao", parsed.get_vietnamese())
        self.assertTrue(parsed.has_synonym("hi"))

    def test_word_limits_synonyms(self):
        # Số synonym không được vượt quá MAX_SYNONYMS trong AppConfig
        word = Word("run", "chay")
        synonym_values = [
            "jog",
            "sprint",
            "dash",
            "race",
            "hurry",
            "rush",
            "speed",
            "bolt",
            "scamper",
            "canter",
            "lope",
            "trot",
        ]

        for synonym in synonym_values:
            word.add_synonym(synonym)

        self.assertEqual(AppConfig.MAX_SYNONYMS, word.get_synonym_count())

    def test_bad_file_line_returns_none(self):
        # Dòng sai định dạng phải trả về None thay vì tạo Word lỗi
        self.assertIsNone(Word.from_file_line("bad line"))
