# Test Word model - Kiểm tra model Word

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.AppConfig import AppConfig
from models.Word import Word


class TestWord(unittest.TestCase):
    """Test Suite: Kiểm tra model Word"""

    def setUp(self):
        self.word = Word("Hello", "Xin chào", "Hello, how are you?", ["hi", "hey"])

    # --- Khởi tạo ---

    def test_create_word(self):
        """Tạo word với đầy đủ thuộc tính"""
        self.assertEqual(self.word.get_english(), "hello")
        self.assertEqual(self.word.get_vietnamese(), "Xin chào")
        self.assertEqual(self.word.get_example(), "Hello, how are you?")
        self.assertEqual(self.word.get_synonyms(), ["hi", "hey"])

    def test_create_word_normalizes_english(self):
        """English phải được normalize về chữ thường, bỏ khoảng trắng thừa"""
        w = Word("  HELLO  WORLD  ", "Nghĩa")
        self.assertEqual(w.get_english(), "hello world")

    def test_create_word_empty(self):
        """Word rỗng không crash"""
        w = Word()
        self.assertEqual(w.get_english(), "")
        self.assertEqual(w.get_vietnamese(), "")
        self.assertEqual(w.get_example(), "")
        self.assertEqual(w.get_synonyms(), [])

    # --- Setters ---

    def test_set_english(self):
        self.word.set_english("Goodbye")
        self.assertEqual(self.word.get_english(), "goodbye")

    def test_set_vietnamese(self):
        self.word.set_vietnamese("Tạm biệt")
        self.assertEqual(self.word.get_vietnamese(), "Tạm biệt")

    def test_set_example(self):
        self.word.set_example("Goodbye!")
        self.assertEqual(self.word.get_example(), "Goodbye!")

    # --- Synonym ---

    def test_add_synonym_success(self):
        """Thêm synonym hợp lệ"""
        result = self.word.add_synonym("greetings")
        self.assertTrue(result)
        self.assertIn("greetings", self.word.get_synonyms())

    def test_add_synonym_duplicate_rejected(self):
        """Không thêm synonym trùng"""
        result = self.word.add_synonym("hi")
        self.assertFalse(result)
        # Đảm bảo không bị thêm 2 lần
        self.assertEqual(self.word.get_synonym_count(), 2)

    def test_add_synonym_invalid_rejected(self):
        """Không thêm synonym có số hoặc ký tự đặc biệt"""
        result = self.word.add_synonym("hi123")
        self.assertFalse(result)

    def test_add_synonym_max_limit(self):
        """Không vượt quá MAX_SYNONYMS"""
        w = Word("test", "nghĩa")
        for i in range(AppConfig.MAX_SYNONYMS):
            # Dùng từ hợp lệ (chỉ chữ cái)
            w.add_synonym(chr(ord("a") + (i % 26)) + chr(ord("a") + ((i + 1) % 26)))
        # Lần thứ MAX_SYNONYMS + 1 phải bị từ chối
        result = w.add_synonym("overflow")
        self.assertFalse(result)
        self.assertEqual(w.get_synonym_count(), AppConfig.MAX_SYNONYMS)

    def test_has_synonym(self):
        self.assertTrue(self.word.has_synonym("hi"))
        self.assertTrue(self.word.has_synonym("HI"))
        self.assertFalse(self.word.has_synonym("bye"))

    def test_get_synonym_count(self):
        self.assertEqual(self.word.get_synonym_count(), 2)

    # --- Serialization ---

    def test_to_file_line(self):
        """Chuyển Word thành dòng file với FIELD_SEPARATOR"""
        line = self.word.to_file_line()
        self.assertIn(AppConfig.FIELD_SEPARATOR, line)
        parts = line.split(AppConfig.FIELD_SEPARATOR)
        self.assertEqual(parts[0], "hello")
        self.assertEqual(parts[1], "Xin chào")
        self.assertEqual(parts[2], "Hello, how are you?")
        # Synonyms dùng LIST_SEPARATOR
        self.assertEqual(parts[3], "hi,hey")

    def test_from_file_line_valid(self):
        """Parse dòng file hợp lệ thành Word"""
        line = "hello|Xin chào|Hello, how are you?|hi,hey"
        w = Word.from_file_line(line)
        self.assertIsNotNone(w)
        self.assertEqual(w.get_english(), "hello")
        self.assertEqual(w.get_vietnamese(), "Xin chào")
        self.assertIn("hi", w.get_synonyms())
        self.assertIn("hey", w.get_synonyms())

    def test_from_file_line_invalid(self):
        """Dòng file không hợp lệ trả về None"""
        self.assertIsNone(Word.from_file_line(""))
        self.assertIsNone(Word.from_file_line(None))
        # Thiếu field
        self.assertIsNone(Word.from_file_line("hello|nghĩa"))

    def test_roundtrip_serialization(self):
        """to_file_line → from_file_line phải khớp"""
        line = self.word.to_file_line()
        restored = Word.from_file_line(line)
        self.assertIsNotNone(restored)
        self.assertEqual(restored.get_english(), self.word.get_english())
        self.assertEqual(restored.get_vietnamese(), self.word.get_vietnamese())
        self.assertEqual(restored.get_example(), self.word.get_example())
        self.assertEqual(restored.get_synonyms(), self.word.get_synonyms())


if __name__ == "__main__":
    unittest.main()
