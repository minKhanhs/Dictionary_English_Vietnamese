# Kiểm thử

## 1. Mục tiêu kiểm thử

- Kiểm tra tính đúng đắn của các module trong chương trình từ điển Anh - Việt.
- Tách rõ kiểm thử đơn vị và kiểm thử tích hợp mức service.
- Kiểm tra các chức năng đã được triển khai trong code: thêm từ, tra cứu, tìm kiếm gần đúng, lịch sử, yêu thích và xóa từ.
- Kiểm tra xử lý dữ liệu rỗng, dữ liệu trùng và dữ liệu không hợp lệ.

## 2. Phạm vi kiểm thử

Phần kiểm thử được tổ chức trong thư mục `tests/`:

```text
tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── TestArrayList.py
│   ├── TestFavoriteList.py
│   ├── TestFuzzySearch.py
│   ├── TestHistoryList.py
│   ├── TestTrie.py
│   ├── TestValidation.py
│   └── TestWord.py
└── integration/
    ├── __init__.py
    └── TestDictionaryService.py
```

Các nhóm kiểm thử:

- Unit test cho cấu trúc dữ liệu: `ArrayList`, `Trie`.
- Unit test cho model và danh sách dữ liệu: `Word`, `HistoryList`, `FavoriteList`.
- Unit test cho validation: `Validation`.
- Unit test cho thuật toán: `Levenshtein`, `FuzzySearch`.
- Integration test mức service cho `DictionaryService`.

Các phần chưa có trong phạm vi kiểm thử tự động:

- Kiểm thử tự động cho giao diện console `Menu` và `MenuHandler`.
- Kiểm thử end-to-end từ nhập liệu người dùng đến lưu/đọc file.
- Kiểm thử hiệu năng với dữ liệu lớn.

## 3. Môi trường kiểm thử

- Ngôn ngữ: Python.
- Công cụ kiểm thử: `unittest`.
- Test runner: `python -m unittest discover`.
- Dữ liệu kiểm thử: dữ liệu mẫu được khai báo trực tiếp trong từng file test.

Các lệnh chạy test:

```bash
.venv/bin/python -m unittest discover -s tests/unit -p "Test*.py"
.venv/bin/python -m unittest discover -s tests/integration -p "Test*.py"
.venv/bin/python -m unittest discover -s tests -p "Test*.py"
```

Trong `main.py`, lựa chọn `2. Chạy test suite` gọi `unittest.TestLoader().discover("tests", pattern="Test*.py")` để chạy toàn bộ test suite.

## 4. Unit test

### 4.1. Mục đích unit test

Unit test kiểm tra từng lớp hoặc nhóm hàm độc lập. Các test này tập trung vào logic nội bộ của từng module, chưa kiểm tra toàn bộ luồng console.

### 4.2. Danh sách module được unit test

| File test | Module được kiểm thử |
|---|---|
| `tests/unit/TestArrayList.py` | `structures/ArrayList.py` |
| `tests/unit/TestTrie.py` | `structures/Trie.py` |
| `tests/unit/TestWord.py` | `models/Word.py` |
| `tests/unit/TestValidation.py` | `validate/Validation.py` |
| `tests/unit/TestHistoryList.py` | `models/HistoryList.py` |
| `tests/unit/TestFavoriteList.py` | `models/FavoriteList.py` |
| `tests/unit/TestFuzzySearch.py` | `algorithms/Levenshtein.py`, `algorithms/FuzzySearch.py` |

### 4.3. Bảng test case unit test

| ID | Module | Mục tiêu kiểm thử | Input | Expected output |
|---|---|---|---|---|
| UT01 | ArrayList | Thêm và lấy phần tử | `hello`, `world` | Lấy đúng phần tử theo index |
| UT02 | ArrayList | Xóa phần tử | List `a, b, c`, xóa index `1` | Trả về `b`, list còn `a, c` |
| UT03 | ArrayList | Xử lý index sai | Index ngoài phạm vi | Phát sinh `IndexError` |
| UT04 | Trie | Tìm từ đã insert | Insert và search `hello` | Trả về `True` |
| UT05 | Trie | Tìm từ chưa insert | Search `world` | Trả về `False` |
| UT06 | Trie | Kiểm tra prefix | Prefix `hel` | Trả về `True` |
| UT07 | Trie | Xóa từ lá | Xóa `hero` | `hero` không còn tìm thấy, các từ khác vẫn còn |
| UT08 | Trie | Xóa từ là prefix | Xóa `hell` khi có `hello` | `hell` bị xóa, `hello` vẫn còn |
| UT09 | Trie | Xóa từ có chung prefix | Xóa `cat` khi có `car` | `cat` bị xóa, `car` vẫn còn |
| UT10 | Trie | Xóa từ invalid/không tồn tại | Xóa `hello-world`, `world`, chuỗi rỗng | Trả về `False`, dữ liệu cũ giữ nguyên |
| UT11 | Word | Chuẩn hóa english | `Hello` | Lưu thành `hello` |
| UT12 | Word | Thêm nghĩa mới | `book` thêm `đặt chỗ` | Nghĩa mới được nối vào danh sách nghĩa |
| UT13 | Word | Chống trùng synonym | Thêm lại `hi` | Không thêm trùng |
| UT14 | Validation | Từ tiếng Anh hợp lệ | `hello` | Trả về `True` |
| UT15 | Validation | Từ tiếng Anh không hợp lệ | `hello123` | Trả về `False` |
| UT16 | Validation | Lựa chọn menu hợp lệ | `0`, `5`, `11` | Trả về `True` |
| UT17 | HistoryList | Chuẩn hóa lịch sử | `HELLO` | Lưu thành `hello` |
| UT18 | HistoryList | Giới hạn lịch sử | Thêm vượt `MAX_HISTORY_SIZE` | Xóa phần tử cũ nhất |
| UT19 | FavoriteList | Thêm favorite | `hello` | Danh sách có `hello` |
| UT20 | FavoriteList | Chống trùng favorite | Thêm `hello` hai lần | Lần hai bị từ chối |
| UT21 | Levenshtein | Tính hàng khoảng cách | Target `cat`, ký tự `c` | Row tiếp theo đúng |
| UT22 | FuzzySearch | Gợi ý từ gần đúng | `helo` | Gợi ý có `hello` |

### 4.4. Cách chạy unit test

```bash
.venv/bin/python -m unittest discover -s tests/unit -p "Test*.py"
```

### 4.5. Đánh giá unit test

- Các module cấu trúc dữ liệu có test cho thêm, lấy, xóa, tìm kiếm và xử lý dữ liệu sai.
- Các module model/list có test cho chuẩn hóa dữ liệu, chống trùng, giới hạn danh sách và chuyển đổi dữ liệu.
- Thuật toán tìm kiếm gần đúng có test cho Levenshtein và giới hạn số lượng gợi ý.
- Unit test hiện tập trung vào module độc lập, không kiểm tra luồng nhập/xuất console.

## 5. Kiểm thử tích hợp

### 5.1. Mục đích kiểm thử tích hợp

Kiểm thử tích hợp hiện có ở mức service. Nhóm test này kiểm tra `DictionaryService` khi phối hợp với các thành phần bên dưới như `ArrayList`, `Trie`, `HistoryList`, `FavoriteList` và `FuzzySearch`.

### 5.2. Danh sách luồng kiểm thử

Các luồng được kiểm thử trong `tests/integration/TestDictionaryService.py`:

- Thêm từ mới vào từ điển.
- Từ chối thêm từ trùng.
- Import từ mới.
- Import từ trùng và merge nghĩa/từ đồng nghĩa.
- Load dữ liệu từ `FakeFileService`.
- Kiểm tra từ tồn tại.
- Tra cứu chính xác.
- Ghi lịch sử khi tra cứu chính xác thành công.
- Không ghi lịch sử khi tra cứu thất bại.
- Tìm kiếm gần đúng.
- Thêm từ đồng nghĩa thông qua `Word`.
- Xóa từ khỏi từ điển.
- Xóa từ khỏi Favorites khi từ bị xóa khỏi từ điển.
- Giữ nguyên các từ khác sau khi xóa một từ.
- Giữ nguyên từ có chung prefix khi xóa từ ngắn/dài trong Trie.
- Làm mới cache `FuzzySearch` để từ đã xóa không còn xuất hiện trong gợi ý.
- Thêm, xóa và chống trùng Favorites.

### 5.3. Bảng kịch bản kiểm thử tích hợp

| ID | Tên luồng | Các bước thực hiện | Kết quả mong đợi |
|---|---|---|---|
| IT01 | Thêm từ mới | Tạo `Word("computer", ...)`, gọi `addWordObject()` | Thêm thành công và `wordExists("computer")` trả `True` |
| IT02 | Chống trùng từ | Thêm lại `hello` | `addWordObject()` trả `False` |
| IT03 | Import từ mới | Gọi `importWordObject()` với từ chưa tồn tại | Từ được thêm và tra cứu được |
| IT04 | Import từ trùng | Import `book` với nghĩa mới | Nghĩa mới được merge vào từ cũ |
| IT05 | Load dữ liệu | Dùng `FakeFileService`, gọi `loadData()` | Dữ liệu được nạp và từ trùng được merge |
| IT06 | Tra cứu chính xác | Gọi `searchExact("hello")` | Trả về `Word` của `hello` |
| IT07 | Lịch sử tra cứu | Tra cứu thành công `hello` | `HistoryList` có thêm `hello` |
| IT08 | Tìm kiếm gần đúng | Gọi `searchApproximate("helo")` | Danh sách gợi ý có `hello` |
| IT09 | Xóa từ | Gọi `deleteWord("hello")` | Từ bị xóa khỏi Trie và không còn tìm thấy |
| IT10 | Favorites khi xóa từ | Thêm `cat` vào favorites rồi xóa `cat` | `cat` bị xóa khỏi favorites |
| IT11 | Xóa từ chung prefix | Thêm `hell`, xóa `hell` hoặc `hello` | Từ bị xóa mất, từ chung prefix còn lại vẫn tìm được |
| IT12 | Cache fuzzy sau xóa | Search approximate để tạo cache, xóa `hello`, search lại `helo` | Gợi ý không còn chứa `hello` |

### 5.4. Cách chạy integration test

```bash
.venv/bin/python -m unittest discover -s tests/integration -p "Test*.py"
```

### 5.5. Đánh giá kiểm thử tích hợp

- Integration test được tách vào `tests/integration/`.
- `TestDictionaryService.py` kiểm tra tầng service khi phối hợp nhiều module bên dưới.
- Nhóm test này chưa chạy qua giao diện console `Menu`/`MenuHandler`; phạm vi hiện tại dừng ở mức service.

## 6. Tổng kết kiểm thử

- Test được tách thành hai nhóm: `tests/unit/` và `tests/integration/`.
- `tests/unit/` chứa các test cho module độc lập.
- `tests/integration/` chứa test tích hợp mức service cho `DictionaryService`.
- `main.py` có lựa chọn `2. Chạy test suite` để chạy toàn bộ test suite qua `unittest`.
- Tài liệu này chỉ mô tả cấu trúc và phạm vi kiểm thử, không ghi biên bản kết quả chạy test.
