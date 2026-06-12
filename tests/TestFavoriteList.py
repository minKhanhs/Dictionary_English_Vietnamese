import unittest

from models.FavoriteList import FavoriteList


class TestFavoriteList(unittest.TestCase):
    """Kiểm tra FavoriteList (danh sách từ yêu thích)."""

    def setUp(self):
        self.fav = FavoriteList()

    def testAddSuccess(self):
        self.assertTrue(self.fav.add("hello"))
        self.assertEqual(self.fav.getCount(), 1)

    def testAddNormalizes(self):
        self.fav.add("  HELLO  ")
        self.assertTrue(self.fav.contains("hello"))
        self.assertEqual(self.fav.getItem(0), "hello")

    def testAddDuplicateRejected(self):
        self.fav.add("hello")
        self.assertFalse(self.fav.add("hello"))
        self.assertEqual(self.fav.getCount(), 1)

    def testAddDuplicateCaseInsensitive(self):
        self.fav.add("hello")
        self.assertFalse(self.fav.add("HELLO"))
        self.assertEqual(self.fav.getCount(), 1)

    def testAddEmptyRejected(self):
        self.assertFalse(self.fav.add(""))
        self.assertFalse(self.fav.add(None))

    def testRemoveSuccess(self):
        self.fav.add("hello")
        self.assertTrue(self.fav.remove("hello"))
        self.assertEqual(self.fav.getCount(), 0)

    def testRemoveNotFound(self):
        self.assertFalse(self.fav.remove("hello"))

    def testRemoveCaseInsensitive(self):
        self.fav.add("hello")
        self.assertTrue(self.fav.remove("HELLO"))
        self.assertEqual(self.fav.getCount(), 0)

    def testContainsTrue(self):
        self.fav.add("hello")
        self.assertTrue(self.fav.contains("hello"))
        self.assertTrue(self.fav.contains("HELLO"))

    def testContainsFalse(self):
        self.assertFalse(self.fav.contains("hello"))

    def testGetItemValid(self):
        self.fav.add("hello")
        self.fav.add("world")
        self.assertEqual(self.fav.getItem(0), "hello")
        self.assertEqual(self.fav.getItem(1), "world")

    def testGetItemOutOfBounds(self):
        self.assertIsNone(self.fav.getItem(0))
        self.assertIsNone(self.fav.getItem(-1))

    def testClear(self):
        self.fav.add("hello")
        self.fav.add("world")
        self.fav.clear()
        self.assertEqual(self.fav.getCount(), 0)
        self.assertEqual(self.fav.toList(), [])

    def testToList(self):
        self.fav.add("a")
        self.fav.add("b")
        result = self.fav.toList()
        self.assertEqual(result, ["a", "b"])
        result.append("c")
        self.assertEqual(self.fav.getCount(), 2)

    def testToListEmpty(self):
        self.assertEqual(self.fav.toList(), [])

    def testAddRemoveAdd(self):
        self.fav.add("hello")
        self.fav.remove("hello")
        self.assertTrue(self.fav.add("hello"))
        self.assertEqual(self.fav.getCount(), 1)


if __name__ == "__main__":
    unittest.main()
