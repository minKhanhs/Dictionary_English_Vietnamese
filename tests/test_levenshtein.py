import unittest

from algorithms.Levenshtein import Levenshtein


class LevenshteinTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra thuật toán Levenshtein và các hàm tính hàng DP
    """
    def test_distance_for_same_word_is_zero(self):
        # Hai từ giống nhau hoàn toàn phải có khoảng cách bằng 0
        self.assertEqual(0, Levenshtein("hello").distance("hello"))

    def test_distance_handles_one_insertion(self):
        # "helo" thiếu 1 ký tự so với "hello", nên khoảng cách là 1
        self.assertEqual(1, Levenshtein("hello").distance("helo"))

    def test_distance_handles_one_deletion(self):
        # "hello" nhiều hơn "helo" 1 ký tự, nên khoảng cách là 1
        self.assertEqual(1, Levenshtein("helo").distance("hello"))

    def test_distance_handles_one_substitution(self):
        # "cat" và "cut" khác 1 ký tự, nên khoảng cách là 1
        self.assertEqual(1, Levenshtein("cat").distance("cut"))

    def test_distance_handles_multiple_edits(self):
        # Ví dụ kinh điển: "kitten" -> "sitting" cần 3 thao tác
        self.assertEqual(3, Levenshtein("kitten").distance("sitting"))

    def test_initial_row_matches_target_word_length(self):
        # Từ "cat" có độ dài 3, hàng khởi tạo phải là [0, 1, 2, 3]
        self.assertEqual([0, 1, 2, 3], Levenshtein("cat").getInitialRow())

    def test_calculate_next_row_for_matching_character(self):
        # Khi ký tự đầu tiên khớp chữ "c", chi phí tại vị trí tương ứng phải là 0
        levenshtein = Levenshtein("cat")

        next_row = levenshtein.calculateNextRow(levenshtein.getInitialRow(), "c")

        self.assertEqual(0, next_row[1])
        self.assertEqual([1, 0, 1, 2], next_row)

    def test_calculate_next_row_for_mismatching_character(self):
        # Khi ký tự "b" không khớp ký tự nào ở đầu "cat", chi phí phải tăng đúng quy tắc
        levenshtein = Levenshtein("cat")

        next_row = levenshtein.calculateNextRow(levenshtein.getInitialRow(), "b")

        self.assertEqual([1, 1, 2, 3], next_row)
