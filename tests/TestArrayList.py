import unittest

from structures.ArrayList import ArrayList


class TestArrayList(unittest.TestCase):
    """Kiểm tra ArrayList (mảng động)."""

    def setUp(self):
        self.arr = ArrayList()

    def testAddAndGet(self):
        self.arr.add("hello")
        self.arr.add("world")
        self.assertEqual(self.arr.get(0), "hello")
        self.assertEqual(self.arr.get(1), "world")

    def testAddMultiple(self):
        for i in range(15):
            self.arr.add(i)
        self.assertEqual(self.arr.size(), 15)
        self.assertEqual(self.arr.get(14), 14)

    def testGetOutOfBounds(self):
        with self.assertRaises(IndexError):
            self.arr.get(0)
        self.arr.add("x")
        with self.assertRaises(IndexError):
            self.arr.get(1)

    def testSizeEmpty(self):
        self.assertEqual(self.arr.size(), 0)

    def testSizeAfterAdd(self):
        self.arr.add("a")
        self.arr.add("b")
        self.assertEqual(self.arr.size(), 2)

    def testRemoveMiddle(self):
        self.arr.add("a")
        self.arr.add("b")
        self.arr.add("c")
        self.arr.remove(1)
        self.assertEqual(self.arr.size(), 2)
        self.assertEqual(self.arr.get(0), "a")
        self.assertEqual(self.arr.get(1), "c")

    def testRemoveLast(self):
        self.arr.add("a")
        self.arr.add("b")
        self.arr.remove(1)
        self.assertEqual(self.arr.size(), 1)
        self.assertEqual(self.arr.get(0), "a")

    def testRemoveOutOfBounds(self):
        with self.assertRaises(IndexError):
            self.arr.remove(0)

    def testContainsTrue(self):
        self.arr.add("hello")
        self.assertTrue(self.arr.contains("hello"))

    def testContainsFalse(self):
        self.arr.add("hello")
        self.assertFalse(self.arr.contains("world"))

    def testContainsEmpty(self):
        self.assertFalse(self.arr.contains("anything"))

    def testToString(self):
        self.arr.add("a")
        self.arr.add("b")
        self.assertIn("a", self.arr.toString())

    def testAddNone(self):
        self.arr.add(None)
        self.assertIsNone(self.arr.get(0))

    def testResize(self):
        for i in range(20):
            self.arr.add(i)
        self.assertEqual(self.arr.size(), 20)
        for i in range(20):
            self.assertEqual(self.arr.get(i), i)


if __name__ == "__main__":
    unittest.main()
