import unittest

from config.AppConfig import AppConfig
from models.Word import Word


class TestWord(unittest.TestCase):
    """Kiểm tra model Word."""

    def setUp(self):
        self.word = Word("Hello", "Xin chào", "Hello, how are you?", ["hi", "hey"])

    def testCreate(self):
        self.assertEqual(self.word.getEnglish(), "hello")
        self.assertEqual(self.word.getVietnamese(), "Xin chào")
        self.assertEqual(self.word.getExample(), "Hello, how are you?")
        self.assertEqual(self.word.getSynonyms(), ["hi", "hey"])

    def testNormalizeEnglish(self):
        w = Word("  HELLO  WORLD  ", "Nghĩa")
        self.assertEqual(w.getEnglish(), "hello world")

    def testCreateEmpty(self):
        w = Word()
        self.assertEqual(w.getEnglish(), "")
        self.assertEqual(w.getVietnamese(), "")
        self.assertEqual(w.getExample(), "")
        self.assertEqual(w.getSynonyms(), [])

    def testSetEnglish(self):
        self.word.setEnglish("Goodbye")
        self.assertEqual(self.word.getEnglish(), "goodbye")

    def testSetVietnamese(self):
        self.word.setVietnamese("Tạm biệt")
        self.assertEqual(self.word.getVietnamese(), "Tạm biệt")

    def testSetExample(self):
        self.word.setExample("Goodbye!")
        self.assertEqual(self.word.getExample(), "Goodbye!")

    def testAddSynonymSuccess(self):
        result = self.word.addSynonym("greetings")
        self.assertTrue(result)
        self.assertIn("greetings", self.word.getSynonyms())

    def testAddSynonymDuplicate(self):
        result = self.word.addSynonym("hi")
        self.assertFalse(result)
        self.assertEqual(self.word.getSynonymCount(), 2)

    def testAddSynonymInvalid(self):
        result = self.word.addSynonym("hi123")
        self.assertFalse(result)

    def testAddSynonymMaxLimit(self):
        w = Word("test", "nghĩa")
        for i in range(AppConfig.MAX_SYNONYMS):
            w.addSynonym(chr(ord("a") + (i % 26)) + chr(ord("a") + ((i + 1) % 26)))
        result = w.addSynonym("overflow")
        self.assertFalse(result)
        self.assertEqual(w.getSynonymCount(), AppConfig.MAX_SYNONYMS)

    def testHasSynonym(self):
        self.assertTrue(self.word.hasSynonym("hi"))
        self.assertTrue(self.word.hasSynonym("HI"))
        self.assertFalse(self.word.hasSynonym("bye"))

    def testGetSynonymCount(self):
        self.assertEqual(self.word.getSynonymCount(), 2)

    def testToFileLine(self):
        line = self.word.toFileLine()
        self.assertIn(AppConfig.FIELD_SEPARATOR, line)
        parts = line.split(AppConfig.FIELD_SEPARATOR)
        self.assertEqual(parts[0], "hello")
        self.assertEqual(parts[1], "Xin chào")
        self.assertEqual(parts[3], "hi,hey")

    def testFromFileLineValid(self):
        line = "hello|Xin chào|Hello, how are you?|hi,hey"
        w = Word.fromFileLine(line)
        self.assertIsNotNone(w)
        assert w is not None
        self.assertEqual(w.getEnglish(), "hello")
        self.assertIn("hi", w.getSynonyms())

    def testFromFileLineInvalid(self):
        self.assertIsNone(Word.fromFileLine(""))
        self.assertIsNone(Word.fromFileLine(None))
        self.assertIsNone(Word.fromFileLine("hello|nghĩa"))

    def testRoundtrip(self):
        line = self.word.toFileLine()
        restored = Word.fromFileLine(line)
        self.assertIsNotNone(restored)
        assert restored is not None
        self.assertEqual(restored.getEnglish(), self.word.getEnglish())
        self.assertEqual(restored.getVietnamese(), self.word.getVietnamese())
        self.assertEqual(restored.getExample(), self.word.getExample())
        self.assertEqual(restored.getSynonyms(), self.word.getSynonyms())


if __name__ == "__main__":
    unittest.main()
