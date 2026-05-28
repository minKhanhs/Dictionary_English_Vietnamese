import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config.AppConfig import AppConfig
from structures.Trie import TrieNode
from algorithms.Levenshtein import Levenshtein
from algorithms.FuzzySearch import FuzzySearch

class TestLevenshtein(unittest.TestCase):
    """
    Test Suite 1: Kiểm tra tính toán cốt lõi của thuật toán Levenshtein
    """
    def setUp(self):
        # Thiết lập trước mỗi test case
        self.targetWord = "cat"
        self.lev = Levenshtein(self.targetWord)

    def testGetInitialRow(self):
        # Từ "cat" có độ dài 3 -> Hàng khởi tạo phải là [0, 1, 2, 3]
        expectedRow = [0, 1, 2, 3]
        self.assertEqual(self.lev.getInitialRow(), expectedRow)

    def testCalculateNextRowMatch(self):
        # Khi ký tự khớp hoàn toàn (chữ 'c' đầu tiên)
        initialRow = self.lev.getInitialRow() # [0, 1, 2, 3]
        nextRow = self.lev.calculateNextRow(initialRow, 'c')
        
        # Chi phí ở vị trí tương ứng (index 1) phải là 0 vì 'c' == 'c'
        self.assertEqual(nextRow[1], 0)
        # Kết quả mong đợi của cả hàng khi xét chữ 'c' với "cat"
        self.assertEqual(nextRow, [1, 0, 1, 2])

    def testCalculateNextRowMismatch(self):
        # Khi ký tự không khớp (chữ 'b')
        initialRow = self.lev.getInitialRow()
        nextRow = self.lev.calculateNextRow(initialRow, 'b')
        
        # Vì khác biệt hoàn toàn, chi phí phải tăng lên
        self.assertEqual(nextRow, [1, 1, 2, 3])


class TestFuzzySearch(unittest.TestCase):
    """
    Test Suite 2: Kiểm tra logic tìm kiếm gần đúng trên cây Trie
    """
    def setUp(self):
        # 1. Khởi tạo cây Trie giả lập
        self.trieRoot = TrieNode()
        self.dictionaryWords = [
            "hello", "hell", "helicopter", "hero", 
            "help", "healer", "halo", "cat", "car"
        ]
        for word in self.dictionaryWords:
            self.trieRoot.insert(word)

        # 2. Khởi tạo bộ tìm kiếm
        self.matcher = FuzzySearch(self.trieRoot)

    def testGetMaxDistanceLogic(self):
        # Kiểm tra xem hàm lấy ngưỡng có tuân thủ đúng AppConfig không
        # SHORT_WORD_LENGTH = 4, SHORT_WORD_DISTANCE = 1
        self.assertEqual(self.matcher.getMaxDistance(3), AppConfig.SHORT_WORD_DISTANCE)
        self.assertEqual(self.matcher.getMaxDistance(4), AppConfig.SHORT_WORD_DISTANCE)
        
        # MEDIUM_WORD_LENGTH = 8, MEDIUM_WORD_DISTANCE = 2
        self.assertEqual(self.matcher.getMaxDistance(6), AppConfig.MEDIUM_WORD_DISTANCE)

    def testExactMatch(self):
        # Nếu nhập đúng từ có trong từ điển, nó phải nằm đầu kết quả
        suggestions = self.matcher.getSuggestions("hello")
        self.assertTrue(len(suggestions) > 0)
        self.assertEqual(suggestions[0], "hello")

    def testTypoMatchShortWord(self):
        # Từ "helo" (sai 1 lỗi) -> độ dài 4 -> max distance = 1
        # Các từ mong đợi: "hell", "hello", "halo", "hero", "help"
        suggestions = self.matcher.getSuggestions("helo")
        self.assertIn("hello", suggestions)
        self.assertIn("hell", suggestions)

    def testExceedMaxDistance(self):
        # Từ "xyz" độ dài 3 -> max distance = 1
        # Trong từ điển không có từ nào gần với "xyz" trong khoảng cách 1
        suggestions = self.matcher.getSuggestions("xyz")
        self.assertEqual(len(suggestions), 0)

    def testMaxSuggestionsLimit(self):
        # Lấy thử một từ ngắn để hệ thống trả về nhiều kết quả
        suggestions = self.matcher.getSuggestions("hel")
        # Kết quả trả về không được vượt quá MAX_SUGGESTIONS định nghĩa trong AppConfig
        self.assertTrue(len(suggestions) <= AppConfig.MAX_SUGGESTIONS)

    def testEmptyString(self):
        # Chuỗi rỗng phải trả về danh sách rỗng, không được lỗi crash (Exception)
        self.assertEqual(self.matcher.getSuggestions(""), [])

if __name__ == "__main__":
    unittest.main()