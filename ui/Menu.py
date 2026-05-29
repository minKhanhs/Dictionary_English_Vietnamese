# UI Menu - Giao diện menu console cho từ điển Anh-Việt

from config.AppConfig import AppConfig
from services.DictionaryService import DictionaryService
from validate.Validation import Validation


class Menu:
    """Giao diện menu console. Chỉ gọi DictionaryService, không xử lý nghiệp vụ."""

    def __init__(self, dictionary_service=None):
        self.dictionary_service = dictionary_service or DictionaryService()

    def show_main_menu(self):
        print("\n===== TỪ ĐIỂN ANH - VIỆT =====")
        print("1.  Thêm từ mới")
        print("2.  Thêm từ đồng nghĩa")
        print("3.  Tra cứu chính xác")
        print("4.  Tìm kiếm gần đúng")
        print("5.  Hiển thị lịch sử tra cứu")
        print("6.  Thêm từ vào Favorites")
        print("7.  Xóa từ khỏi Favorites")
        print("8.  Hiển thị Favorites")
        print("9.  Hiển thị tất cả từ")
        print("10. Lưu dữ liệu")
        print("11. Xóa từ điển")
        print("0.  Thoát")

    def input_choice(self):
        """Nhập lựa chọn menu. Xử lý nhập sai kiểu."""
        while True:
            choice = input("Chọn chức năng: ")
            if Validation.isValidMenuOption(choice):
                return int(choice)
            print("Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 11.")

    def run(self):
        """Vòng lặp menu chính."""
        self.dictionary_service.load_data()
        while True:
            self.show_main_menu()
            choice = self.input_choice()
            if choice == 1:
                self.dictionary_service.add_word_interactive()
            elif choice == 2:
                self.dictionary_service.add_synonym_interactive()
            elif choice == 3:
                self.dictionary_service.search_exact_interactive()
            elif choice == 4:
                self.dictionary_service.search_approximate_interactive()
            elif choice == 5:
                self.dictionary_service.show_history()
            elif choice == 6:
                self.dictionary_service.add_favorite_interactive()
            elif choice == 7:
                self.dictionary_service.remove_favorite_interactive()
            elif choice == 8:
                self.dictionary_service.show_favorites()
            elif choice == 9:
                self.dictionary_service.display_all_words()
            elif choice == 10:
                if self.dictionary_service.save_data():
                    print("Đã lưu dữ liệu.")
                else:
                    print("Lưu dữ liệu thất bại.")
            elif choice == 11:
                self.dictionary_service.delete_word_interactive()
            elif choice == 0:
                self.dictionary_service.save_data()
                print("Tạm biệt!")
                break
