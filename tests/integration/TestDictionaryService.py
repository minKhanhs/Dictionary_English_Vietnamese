import os
import sys
import unittest

from config.AppConfig import AppConfig
from models.Word import Word
from services.DictionaryService import DictionaryService

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


class TestDictionaryService(unittest.TestCase):
    """Kiểm tra DictionaryService CRUD, search, history, favorites."""

    def setUp(self):
        self.service = DictionaryService()
        self.samples = [
            Word("hello", "Xin chào", "Hello, how are you?", ["hi", "hey"]),
            Word("world", "Thế giới", "The world is beautiful.", []),
            Word("cat", "Con mèo", "The cat is sleeping.", ["kitty"]),
            Word("dog", "Con chó", "The dog is barking.", ["puppy"]),
            Word("book", "Quyển sách", "I read a book.", []),
        ]
        for word in self.samples:
            self.service.addWordObject(word)

    # --- CREATE ---

    def testAddWordSuccess(self):
        word = Word("computer", "Máy tính", "I use a computer.", [])
        self.assertTrue(self.service.addWordObject(word))
        self.assertTrue(self.service.wordExists("computer"))

    def testAddWordDuplicate(self):
        word = Word("hello", "Nghĩa khác", "Example khác", [])
        self.assertFalse(self.service.addWordObject(word))

    def testImportWordNewWord(self):
        word = Word("computer", "Máy tính", "I use a computer.", [])
        self.assertTrue(self.service.importWordObject(word))
        result = self.service.searchExact("computer")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.getVietnamese(), "Máy tính")

    def testImportWordDuplicateMeaningMergesSynonymsOnly(self):
        word = Word("hello", "  xin   chào  ", "Hi!", ["greeting"])
        self.assertTrue(self.service.importWordObject(word))
        result = self.service.searchExact("hello")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.getVietnamese(), "Xin chào")
        self.assertIn("greeting", result.getSynonyms())

    def testImportWordDifferentMeaningAppendsMeaning(self):
        word = Word("book", "đặt chỗ", "Book a room.", [])
        self.assertTrue(self.service.importWordObject(word))
        result = self.service.searchExact("book")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.getVietnamese(), "Quyển sách; đặt chỗ")

    def testImportWordMultiMeaningSkipsExistingMeaning(self):
        word = Word("book", "Quyển sách; ghi sổ; đặt chỗ", "Book a room.", [])
        self.assertTrue(self.service.importWordObject(word))
        result = self.service.searchExact("book")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.getVietnamese(), "Quyển sách; ghi sổ; đặt chỗ")

    def testLoadDataMergesDuplicateEnglishFromFile(self):
        class FakeFileService:
            def loadDictionary(self):
                return [
                    Word("book", "quyển sách", "I read a book.", ["volume"]),
                    Word("book", "quyển sách; đặt chỗ", "Book a room.", ["textbook"]),
                    Word("run", "chạy; vận hành", "They run a company.", []),
                ]

            def loadHistory(self):
                return []

            def loadFavorites(self):
                return []

        service = DictionaryService(FakeFileService())
        service.loadData()
        result = service.searchExact("book")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(service.words.getSize(), 2)
        self.assertEqual(result.getVietnamese(), "quyển sách; đặt chỗ")
        self.assertEqual(result.getExample(), "I read a book.")
        self.assertEqual(result.getSynonyms(), ["volume", "textbook"])

    def testAddWordEmptyEnglish(self):
        self.assertFalse(self.service.addWordObject(Word("", "Nghĩa", "Ví dụ", [])))

    def testAddWordInvalidEnglish(self):
        self.assertFalse(
            self.service.addWordObject(Word("hello123", "Nghĩa", "Ví dụ", []))
        )

    def testAddWordNone(self):
        self.assertFalse(self.service.addWordObject(None))

    # --- READ ---

    def testWordExistsTrue(self):
        self.assertTrue(self.service.wordExists("hello"))
        self.assertTrue(self.service.wordExists("HELLO"))

    def testWordExistsFalse(self):
        self.assertFalse(self.service.wordExists("xyz"))
        self.assertFalse(self.service.wordExists(""))

    def testSearchExactFound(self):
        result = self.service.searchExact("hello")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.getEnglish(), "hello")
        self.assertEqual(result.getVietnamese(), "Xin chào")

    def testSearchExactNotFound(self):
        self.assertIsNone(self.service.searchExact("xyz"))

    def testSearchExactEmpty(self):
        self.assertIsNone(self.service.searchExact(""))

    def testSearchExactAddsToHistory(self):
        self.service.searchExact("hello")
        self.assertEqual(self.service.history.getCount(), 1)
        self.assertEqual(self.service.history.getItem(0), "hello")

    def testSearchExactMissNoHistory(self):
        self.service.searchExact("xyz")
        self.assertEqual(self.service.history.getCount(), 0)

    def testSearchApproximateFound(self):
        results = self.service.searchApproximate("helo")
        englishList = [w.getEnglish() for w in results]
        self.assertIn("hello", englishList)

    def testSearchApproximateNoMatch(self):
        self.assertEqual(self.service.searchApproximate("xyz"), [])

    def testSearchApproximateEmpty(self):
        self.assertEqual(self.service.searchApproximate(""), [])

    def testSearchApproximateMaxLimit(self):
        results = self.service.searchApproximate("hel")
        self.assertTrue(len(results) <= AppConfig.MAX_SUGGESTIONS)

    # --- UPDATE ---

    def testAddSynonymViaWord(self):
        word = self.service.searchExact("book")
        self.assertIsNotNone(word)
        assert word is not None
        self.assertTrue(word.addSynonym("volume"))
        self.assertTrue(word.hasSynonym("volume"))

    # --- DELETE ---

    def testDeleteWordSuccess(self):
        self.assertTrue(self.service.deleteWord("hello"))
        self.assertFalse(self.service.wordExists("hello"))
        self.assertIsNone(self.service._findWord("hello"))

    def testDeleteWordNotFound(self):
        self.assertFalse(self.service.deleteWord("xyz"))

    def testDeleteWordEmpty(self):
        self.assertFalse(self.service.deleteWord(""))

    def testDeleteRemovesFromFavorites(self):
        self.service.favorites.add("cat")
        self.service.deleteWord("cat")
        self.assertFalse(self.service.favorites.contains("cat"))

    def testDeletePreservesOthers(self):
        self.service.deleteWord("cat")
        self.assertTrue(self.service.wordExists("hello"))
        self.assertTrue(self.service.wordExists("dog"))

    # --- HISTORY / FAVORITES ---

    def testHistoryTracksSearches(self):
        self.service.searchExact("hello")
        self.service.searchExact("cat")
        self.assertEqual(self.service.history.getCount(), 2)

    def testFavoritesAddAndContains(self):
        self.service.favorites.add("hello")
        self.assertTrue(self.service.favorites.contains("hello"))

    def testFavoritesRemove(self):
        self.service.favorites.add("hello")
        self.service.favorites.remove("hello")
        self.assertFalse(self.service.favorites.contains("hello"))

    def testFavoritesNoDuplicate(self):
        self.service.favorites.add("hello")
        self.assertFalse(self.service.favorites.add("hello"))

    # --- DISPLAY (no crash) ---

    def testDisplayAllWordsNoCrash(self):
        self.service.getAllWords()

    def testShowHistoryNoCrash(self):
        self.service.getHistory().display()

    def testShowFavoritesNoCrash(self):
        self.service.getFavorites().display()


if __name__ == "__main__":
    unittest.main()
