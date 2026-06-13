import unittest

from structures.ArrayList import ArrayList, DynamicArray


class TestArrayList(unittest.TestCase):
    """Kiểm tra ArrayList (mảng động)."""

    def setUp(self):
        self.arr = ArrayList()

    def testAddAndGet(self):
        self.arr.add("hello")
        self.arr.add("world")
        self.assertEqual(self.arr.get(0), "hello")
        self.assertEqual(self.arr.get(1), "world")

    def testPushBackAlias(self):
        self.arr.add("hello")
        self.assertEqual(self.arr.get(0), "hello")
        self.assertEqual(self.arr.getSize(), 1)

    def testAddMultiple(self):
        for i in range(15):
            self.arr.add(i)
        self.assertEqual(self.arr.getSize(), 15)
        self.assertEqual(self.arr.get(14), 14)

    def testGetOutOfBounds(self):
        with self.assertRaises(IndexError):
            self.arr.get(0)
        self.arr.add("x")
        with self.assertRaises(IndexError):
            self.arr.get(1)

    def testSizeEmpty(self):
        self.assertEqual(self.arr.getSize(), 0)

    def testSizeAfterAdd(self):
        self.arr.add("a")
        self.arr.add("b")
        self.assertEqual(self.arr.getSize(), 2)
        self.assertEqual(self.arr.getSize(), 2)

    def testRemoveMiddle(self):
        self.arr.add("a")
        self.arr.add("b")
        self.arr.add("c")
        removed = self.arr.remove(1)
        self.assertEqual(removed, "b")
        self.assertEqual(self.arr.getSize(), 2)
        self.assertEqual(self.arr.get(0), "a")
        self.assertEqual(self.arr.get(1), "c")

    def testRemoveLast(self):
        self.arr.add("a")
        self.arr.add("b")
        self.arr.remove(1)
        self.assertEqual(self.arr.getSize(), 1)
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
        self.assertIn("a", str(self.arr.toList()))

    def testSet(self):
        self.arr.add("a")
        self.arr.set(0, "b")
        self.assertEqual(self.arr.get(0), "b")

    def testClearAndIsEmpty(self):
        self.arr.add("a")
        self.assertFalse(self.arr.isEmpty())
        self.arr.clear()
        self.assertTrue(self.arr.isEmpty())
        self.assertEqual(self.arr.getSize(), 0)

    def testToListReturnsCopy(self):
        self.arr.add("a")
        result = self.arr.toList()
        result.append("b")
        self.assertEqual(self.arr.getSize(), 1)

    def testPublicCapacityAndData(self):
        self.assertEqual(self.arr.capacity, 10)
        self.assertEqual(len(self.arr.data), self.arr.capacity)

    def testAddNone(self):
        self.arr.add(None)
        self.assertIsNone(self.arr.get(0))

    def testResize(self):
        for i in range(20):
            self.arr.add(i)
        self.assertEqual(self.arr.getSize(), 20)
        for i in range(20):
            self.assertEqual(self.arr.get(i), i)

    def testDynamicArrayAlias(self):
        arr = DynamicArray()
        arr.add("hello")
        self.assertEqual(arr.get(0), "hello")


if __name__ == "__main__":
    unittest.main()
