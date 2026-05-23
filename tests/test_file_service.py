import os
import tempfile
import unittest

from config.app_config import AppConfig
from models.word import Word
from services.file_service import FileService


class FileServiceTest(unittest.TestCase):
    """
    Test Suite: Kiểm tra đọc ghi file dictionary, history và favorites
    """
    def setUp(self):
        # Lưu lại cấu hình thật để test không ghi vào thư mục data chính
        self.original_config = (
            AppConfig.DATA_FOLDER,
            AppConfig.DICTIONARY_FILE,
            AppConfig.HISTORY_FILE,
            AppConfig.FAVORITES_FILE,
        )

        # Tạo thư mục tạm cho từng test case để đảm bảo test độc lập
        self.temp_dir = tempfile.TemporaryDirectory()
        AppConfig.DATA_FOLDER = self.temp_dir.name
        AppConfig.DICTIONARY_FILE = os.path.join(self.temp_dir.name, "dictionary.txt")
        AppConfig.HISTORY_FILE = os.path.join(self.temp_dir.name, "history.txt")
        AppConfig.FAVORITES_FILE = os.path.join(self.temp_dir.name, "favorites.txt")
        self.service = FileService()

    def tearDown(self):
        # Khôi phục cấu hình ban đầu sau mỗi test case
        (
            AppConfig.DATA_FOLDER,
            AppConfig.DICTIONARY_FILE,
            AppConfig.HISTORY_FILE,
            AppConfig.FAVORITES_FILE,
        ) = self.original_config
        self.temp_dir.cleanup()

    def test_ensure_data_folder_creates_dictionary_file(self):
        # ensure_data_folder phải tạo file dictionary nếu chưa tồn tại
        self.service.ensure_data_folder()

        self.assertTrue(os.path.exists(AppConfig.DICTIONARY_FILE))

    def test_missing_dictionary_loads_empty_list(self):
        # Khi file dictionary chưa có dữ liệu, load_dictionary trả về danh sách rỗng
        self.assertEqual([], self.service.load_dictionary())

    def test_bad_dictionary_lines_are_skipped(self):
        # Dòng sai định dạng bị bỏ qua, dòng đúng vẫn được load
        self.service.ensure_data_folder()
        with open(AppConfig.DICTIONARY_FILE, "w", encoding="utf-8") as file:
            file.write("bad line\n")
            file.write("hello|xin chao|Hello!|hi\n")

        self.assertEqual(1, len(self.service.load_dictionary()))

    def test_dictionary_round_trip(self):
        # Word lưu xuống file rồi đọc lại phải giữ đúng từ tiếng Anh
        word = Word("book", "sach", "A book.", ["volume"])

        self.assertTrue(self.service.save_dictionary([word]))
        self.assertEqual("book", self.service.load_dictionary()[0].get_english())

    def test_history_round_trip(self):
        # History lưu xuống file rồi đọc lại phải giữ đúng thứ tự dữ liệu
        self.assertTrue(self.service.save_history(["hello"]))
        self.assertEqual(["hello"], self.service.load_history())

    def test_favorites_round_trip(self):
        # Favorites lưu xuống file rồi đọc lại phải giữ đúng dữ liệu
        self.assertTrue(self.service.save_favorites(["book"]))
        self.assertEqual(["book"], self.service.load_favorites())
