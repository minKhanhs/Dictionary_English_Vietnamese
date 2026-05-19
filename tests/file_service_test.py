import os
import tempfile

from config.app_config import AppConfig
from models.word import Word
from services.file_service import FileService


class FileServiceTest:
    @staticmethod
    def run(runner):
        original = (
            AppConfig.DATA_FOLDER,
            AppConfig.DICTIONARY_FILE,
            AppConfig.HISTORY_FILE,
            AppConfig.FAVORITES_FILE,
        )
        with tempfile.TemporaryDirectory() as folder:
            AppConfig.DATA_FOLDER = folder
            AppConfig.DICTIONARY_FILE = os.path.join(folder, "dictionary.txt")
            AppConfig.HISTORY_FILE = os.path.join(folder, "history.txt")
            AppConfig.FAVORITES_FILE = os.path.join(folder, "favorites.txt")

            service = FileService()
            service.ensure_data_folder()
            runner.assert_true(os.path.exists(AppConfig.DICTIONARY_FILE), "file service creates dictionary")
            runner.assert_equal([], service.load_dictionary(), "missing dictionary loads empty")

            with open(AppConfig.DICTIONARY_FILE, "w", encoding="utf-8") as file:
                file.write("bad line\n")
                file.write("hello|xin chao|Hello!|hi\n")
            runner.assert_equal(1, len(service.load_dictionary()), "bad dictionary line skipped")

            word = Word("book", "sach", "A book.", ["volume"])
            runner.assert_true(service.save_dictionary([word]), "dictionary saves")
            runner.assert_equal("book", service.load_dictionary()[0].get_english(), "dictionary round trip")

            runner.assert_true(service.save_history(["hello"]), "history saves")
            runner.assert_equal(["hello"], service.load_history(), "history round trip")
            runner.assert_true(service.save_favorites(["book"]), "favorites saves")
            runner.assert_equal(["book"], service.load_favorites(), "favorites round trip")

        (
            AppConfig.DATA_FOLDER,
            AppConfig.DICTIONARY_FILE,
            AppConfig.HISTORY_FILE,
            AppConfig.FAVORITES_FILE,
        ) = original
