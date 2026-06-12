from config.ResponseCode import ResponseCode
from services.DictionaryService import DictionaryService
from ui.MenuHandler import MenuHandler
from validate.Validation import Validation


class Menu:
    """Giao diện menu console. Chỉ gọi DictionaryService."""

    def __init__(self, dictionaryService=None):
        self.dictionaryService = dictionaryService or DictionaryService()
        self.handler = MenuHandler(self.dictionaryService)

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
            print(f"[{ResponseCode.INPUT_INVALID}] Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 11.")

    def run(self):
        try:
            self.dictionaryService.loadData()
            print(f"[{ResponseCode.SUCCESS}] Đã tải dữ liệu thành công.")
        except Exception as e:
            print(f"[{ResponseCode.ERROR}] Lỗi tải dữ liệu: {e}")
        while True:
            try:
                self.showMainMenu()
                choice = self.inputChoice()
                if choice == 1:
                    self.handler.addWord()
                elif choice == 2:
                    self.handler.addSynonym()
                elif choice == 3:
                    self.handler.searchExact()
                elif choice == 4:
                    self.handler.searchApproximate()
                elif choice == 5:
                    self.handler.showHistory()
                elif choice == 6:
                    self.handler.addFavorite()
                elif choice == 7:
                    self.handler.removeFavorite()
                elif choice == 8:
                    self.handler.showFavorites()
                elif choice == 9:
                    self.handler.displayAllWords()
                elif choice == 10:
                    if self.dictionaryService.saveData():
                        print(f"[{ResponseCode.SUCCESS}] Đã lưu dữ liệu.")
                    else:
                        print(f"[{ResponseCode.ERROR}] Lưu dữ liệu thất bại.")
                elif choice == 11:
                    self.handler.deleteWord()
                elif choice == 0:
                    self.dictionaryService.saveData()
                    print(f"[{ResponseCode.INFO}] Tạm biệt!")
                    break
            except KeyboardInterrupt:
                print(f"\n[{ResponseCode.CANCELLED}] Đã dừng bởi người dùng.")
                break
            except Exception as e:
                print(f"[{ResponseCode.ERROR}] Lỗi xử lý menu: {e}")
