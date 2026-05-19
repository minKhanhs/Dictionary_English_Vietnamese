from config.app_config import AppConfig
from models.history_list import HistoryList


class HistoryListTest:
    @staticmethod
    def run(runner):
        history = HistoryList()
        runner.assert_equal(0, history.get_count(), "history starts empty")
        for index in range(AppConfig.MAX_HISTORY_SIZE + 3):
            history.add(f"word{index}")
        runner.assert_equal(
            AppConfig.MAX_HISTORY_SIZE, history.get_count(), "history max size"
        )
        runner.assert_equal("word3", history.get_item(0), "history removes oldest")
        history.clear()
        runner.assert_equal([], history.to_list(), "history clears")
