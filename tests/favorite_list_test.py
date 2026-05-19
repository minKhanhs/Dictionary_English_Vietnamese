from models.favorite_list import FavoriteList


class FavoriteListTest:
    @staticmethod
    def run(runner):
        favorites = FavoriteList()
        runner.assert_true(favorites.add("hello"), "favorite add succeeds")
        runner.assert_false(favorites.add("hello"), "favorite duplicate rejected")
        runner.assert_true(favorites.contains("hello"), "favorite contains word")
        runner.assert_equal(1, favorites.get_count(), "favorite count")
        runner.assert_true(favorites.remove("hello"), "favorite remove succeeds")
        runner.assert_false(favorites.contains("hello"), "favorite no longer contains")
        runner.assert_false(favorites.remove("hello"), "favorite remove missing rejected")
