from tests.dictionary_service_test import DictionaryServiceTest
from tests.dynamic_array_test import DynamicArrayTest
from tests.favorite_list_test import FavoriteListTest
from tests.file_service_test import FileServiceTest
from tests.history_list_test import HistoryListTest
from tests.levenshtein_test import LevenshteinTest
from tests.test_runner import TestRunner
from tests.trie_test import TrieTest
from tests.validator_test import ValidatorTest
from tests.word_test import WordTest


class AllTests:
    @staticmethod
    def run_all():
        runner = TestRunner()
        WordTest.run(runner)
        TrieTest.run(runner)
        LevenshteinTest.run(runner)
        ValidatorTest.run(runner)
        DynamicArrayTest.run(runner)
        HistoryListTest.run(runner)
        FavoriteListTest.run(runner)
        FileServiceTest.run(runner)
        DictionaryServiceTest.run(runner)
        return runner.print_summary()


if __name__ == "__main__":
    AllTests.run_all()
