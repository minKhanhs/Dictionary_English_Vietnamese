# Yêu Cầu Và Hiện Trạng Dự Án

## Tổng Quan

Ứng dụng là từ điển Anh-Việt chạy trên console bằng Python. App cho phép quản lý mục từ, tra cứu chính xác bằng Trie, gợi ý gần đúng bằng Levenshtein, lưu lịch sử tra cứu và danh sách yêu thích bằng file text.

Code hiện tại là implementation thuần Python, không dùng database hay thư viện fuzzy-search bên ngoài. Các công cụ ngoài chuẩn chỉ phục vụ phát triển và kiểm tra chất lượng trong `.venv` như `ruff` và `basedpyright`.

## Môi Trường Hiện Tại

| Hạng mục | Hiện trạng |
| --- | --- |
| Runtime | Python 3.14 trong `.venv` |
| Entry point | `main.py` |
| Test framework | `unittest` |
| Static type check | `basedpyright` |
| Lint | `ruff` |
| Persistence | File text ở root repo |

## Cấu Trúc Repository

```text
.
├── main.py
├── algorithms/
├── config/
├── models/
├── services/
├── structures/
├── ui/
├── utils/
├── validate/
├── tests/
├── docs/
├── dictionary.txt
├── history.txt
└── favorites.txt
```

Repo hiện dùng `validate/` thay vì `validation/`. Tên file Python đang theo PascalCase, ví dụ `DictionaryService.py`, `ArrayList.py`, `Validation.py`.

## File Dữ Liệu

`AppConfig` đang cấu hình dữ liệu ở root repo:

```text
dictionary.txt
history.txt
favorites.txt
```

Không có thư mục `data/` trong trạng thái hiện tại. `FileService.ensureDataFiles()` tạo các file thiếu theo đường dẫn trong `AppConfig`, và chỉ tạo thư mục nếu đường dẫn file có folder cha.

## Định Dạng Dictionary

Mỗi dòng trong `dictionary.txt` có 4 field, phân tách bằng `|`:

```text
english|vietnamese|example|synonym1,synonym2,synonym3
```

`AppConfig.MEANING_SEPARATOR` là `;`, nên một từ có nhiều nghĩa sẽ được lưu trong field tiếng Việt:

```text
book|quyển sách; đặt chỗ|Book a room.|volume,textbook
```

`Word.fromFileLine()` bỏ qua dòng không đủ field hoặc có từ tiếng Anh không hợp lệ.

## Chức Năng Đang Có

| Chức năng | Hiện trạng |
| --- | --- |
| Thêm từ mới | Có, qua `MenuHandler.addWord()` và `DictionaryService.addWordObject()` |
| Thêm nghĩa mới cho từ trùng | Có khi import bằng `DictionaryService.importWordObject()` |
| Thêm ví dụ | Có khi tạo `Word`; ví dụ trống được chấp nhận |
| Thêm từ đồng nghĩa | Có, hiện menu gọi trực tiếp `Word.addSynonym()` sau khi tìm từ |
| Tra cứu chính xác | Có, qua `Trie` và `_findWord()` |
| Tìm kiếm gần đúng | Có, qua `FuzzySearch` + `Levenshtein` trên Trie |
| Lưu lịch sử | Có, chỉ ghi khi tra cứu chính xác thành công |
| Favorites | Có thêm/xóa/hiển thị; UI kiểm tra từ tồn tại trước khi thêm |
| Hiển thị toàn bộ từ | Có |
| Xóa từ | Có, menu option 11 gọi `DictionaryService.deleteWord()` |
| Lưu dữ liệu | Có, save dictionary/history/favorites |
| Load dữ liệu | Có, merge các dòng dictionary trùng english |
| Test | Có 147 test bằng `unittest` |

## Luồng Console

Khi chạy `main.py`, chương trình hiển thị:

```text
===== TỪ ĐIỂN ANH - VIỆT =====
1. Chạy ứng dụng
2. Chạy unit test
```

Nếu chọn `2`, app chạy test suite bằng `unittest`. Các lựa chọn khác mặc định chạy ứng dụng.

## Menu Ứng Dụng

| Lựa chọn | Hành động hiện tại |
| --- | --- |
| 1 | Thêm từ mới |
| 2 | Thêm từ đồng nghĩa |
| 3 | Tra cứu chính xác |
| 4 | Tìm kiếm gần đúng |
| 5 | Hiển thị lịch sử tra cứu |
| 6 | Thêm từ vào Favorites |
| 7 | Xóa từ khỏi Favorites |
| 8 | Hiển thị Favorites |
| 9 | Hiển thị tất cả từ |
| 10 | Lưu dữ liệu |
| 11 | Xóa một từ khỏi từ điển |
| 0 | Lưu dữ liệu và thoát |

`AppConfig.MAX_MENU_OPTION` đang là `11`.

## Quy Tắc Validation Hiện Tại

- English word: không rỗng, trong giới hạn độ dài, cho phép chữ cái, dấu cách và dấu gạch ngang.
- Vietnamese meaning: không rỗng, trong giới hạn độ dài.
- Example: được phép rỗng; nếu có thì phải trong giới hạn độ dài.
- Menu option: số nguyên từ `0` đến `11`.
- Dictionary line: phải có ít nhất 4 field, english hợp lệ và nghĩa không rỗng.

## Known Gaps Cần Quyết Định

| Gap | Tác động | Hướng xử lý có thể chọn |
| --- | --- | --- |
| `Validation.isEnglishWord()` cho phép dấu cách và `-`, nhưng `Trie` chỉ nhận `a-z` | Một từ có thể được thêm vào `ArrayList` nhưng không searchable bằng Trie | Siết validation về `a-z`, hoặc mở rộng Trie để hỗ trợ ký tự này |
| Có hai class `Word` ở `models/Word.py` và `structures/Word.py` | Dễ lệch behavior; service dùng `structures.Word`, tests dùng `models.Word` | Hợp nhất một implementation, hoặc ghi rõ ownership |
| Docs cũ nhắc `data/`, code dùng file root | Nếu muốn cấu trúc sạch hơn cần đổi `AppConfig` và migration dữ liệu | Giữ root như hiện tại, hoặc chuyển sang `data/` |
| Ruff đang fail 14 lỗi style/import | Tests vẫn pass nhưng quality gate lint chưa sạch | Sửa code style hoặc không coi Ruff là bắt buộc |

## Cách Chạy

```bash
.venv/bin/python main.py
.venv/bin/python -m unittest discover -s tests -p 'Test*.py'
.venv/bin/basedpyright
.venv/bin/ruff check .
```

## Trạng Thái Kiểm Tra Gần Nhất

| Lệnh | Kết quả |
| --- | --- |
| `.venv/bin/python -m unittest discover -s tests -p 'Test*.py'` | Pass: 147 tests |
| `.venv/bin/basedpyright` | Pass: 0 errors |
| `.venv/bin/ruff check .` | Fail: 14 lint/style issues |
