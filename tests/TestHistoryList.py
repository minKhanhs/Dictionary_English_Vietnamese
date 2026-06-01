import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from config.AppConfig import AppConfig
from models.HistoryList import HistoryList


class TestHistoryList(unittest.TestCase):
    """Kiểm tra HistoryList (lịch sử tra cứu)."""

    def setUp(self):
        self.history = HistoryList()

    def testAddAndGet(self):
        self.history.add("hello")
        self.history.add("world")
        self.assertEqual(self.history.getItem(0), "hello")
        self.assertEqual(self.history.getItem(1), "world")
        self.assertEqual(self.history.getCount(), 2)

    def testAddNormalizes(self):
        self.history.add("  HELLO  ")
        self.assertEqual(self.history.getItem(0), "hello")

    def testAddEmptyRejected(self):
        self.assertFalse(self.history.add(""))
        self.assertEqual(self.history.getCount(), 0)

    def testAddNoneRejected(self):
        self.assertFalse(self.history.add(None))

    def testFifoEviction(self):
        for i in range(AppConfig.MAX_HISTORY_SIZE + 5):
            self.history.add(f"word{i}")
        self.assertEqual(self.history.getCount(), AppConfig.MAX_HISTORY_SIZE)
        self.assertEqual(self.history.getItem(0), "word5")

    def testMaxSizeExact(self):
        for i in range(AppConfig.MAX_HISTORY_SIZE):
            self.history.add(f"word{i}")
        self.assertEqual(self.history.getCount(), AppConfig.MAX_HISTORY_SIZE)
        self.assertEqual(self.history.getItem(0), "word0")

    def testGetItemOutOfBounds(self):
        self.assertIsNone(self.history.getItem(0))
        self.assertIsNone(self.history.getItem(-1))

    def testClear(self):
        self.history.add("hello")
        self.history.add("world")
        self.history.clear()
        self.assertEqual(self.history.getCount(), 0)
        self.assertEqual(self.history.toList(), [])

    def testToList(self):
        self.history.add("a")
        self.history.add("b")
        result = self.history.toList()
        self.assertEqual(result, ["a", "b"])
        result.append("c")
        self.assertEqual(self.history.getCount(), 2)

    def testToListEmpty(self):
        self.assertEqual(self.history.toList(), [])


if __name__ == "__main__":
    unittest.main()
