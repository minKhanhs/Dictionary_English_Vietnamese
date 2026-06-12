from config.ResponseCode import ResponseCode
from services.DictionaryService import DictionaryService
from validate.Validation import Validation


class Menu:
    """Giao diện menu console. Chỉ gọi DictionaryService."""

    def __init__(self, dictionaryService=None):
        self.dictionaryService = dictionaryService or DictionaryService()

    def showMainMenu(self):
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

    def inputChoice(self):
        while True:
            choice = input("Chọn chức năng: ")
            if Validation.isValidMenuOption(choice):
                return int(choice)
            print("Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 11.")

    def run(self):
        try:
            self.dictionaryService.loadData()
        except Exception as e:
            print(f"{ResponseCode.FAIL_LABEL} loadData: {e}")
        while True:
            try:
                self.showMainMenu()
                choice = self.inputChoice()
                if choice == 1:
                    self.dictionaryService.addWordInteractive()
                elif choice == 2:
                    self.dictionaryService.addSynonymInteractive()
                elif choice == 3:
                    self.dictionaryService.searchExactInteractive()
                elif choice == 4:
                    self.dictionaryService.searchApproximateInteractive()
                elif choice == 5:
                    self.dictionaryService.showHistory()
                elif choice == 6:
                    self.dictionaryService.addFavoriteInteractive()
                elif choice == 7:
                    self.dictionaryService.removeFavoriteInteractive()
                elif choice == 8:
                    self.dictionaryService.showFavorites()
                elif choice == 9:
                    self.dictionaryService.displayAllWords()
                elif choice == 10:
                    if self.dictionaryService.saveData():
                        print("Đã lưu dữ liệu.")
                    else:
                        print("Lưu dữ liệu thất bại.")
                elif choice == 11:
                    self.dictionaryService.deleteWordInteractive()
                elif choice == 0:
                    self.dictionaryService.saveData()
                    print("Tạm biệt!")
                    break
            except KeyboardInterrupt:
                print(f"\n{ResponseCode.SKIP_LABEL} Đã dừng bởi người dùng.")
                break
            except Exception as e:
                print(f"{ResponseCode.FAIL_LABEL} Lỗi xử lý menu: {e}")
