# Đặc Tả Module

## Cấu Trúc Yêu Cầu

Cấu trúc mục tiêu ban đầu:

```text
DictionaryProject/
├── main.py
├── config/
├── models/
├── structures/
├── algorithms/
├── services/
├── validation/
├── utils/
├── ui/
├── tests/
└── data/
```

Repository hiện tại dùng tên file PascalCase và dùng `validate/` thay vì `validation/`. Hãy theo style hiện tại của repo trừ khi task yêu cầu đổi tên module rõ ràng.

## Cấu Hình

`config/AppConfig.py` nên chứa toàn bộ hằng số của chương trình, bao gồm:

- Đường dẫn dữ liệu: `DATA_FOLDER`, `DICTIONARY_FILE`, `HISTORY_FILE`, `FAVORITES_FILE`
- Giới hạn: `MAX_SYNONYMS`, `MAX_HISTORY_SIZE`, `MAX_SUGGESTIONS`
- Cấu hình Trie: `ALPHABET_SIZE`, `FIRST_CHAR`, `LAST_CHAR`
- Ngưỡng tìm kiếm gần đúng: `SHORT_WORD_LENGTH`, `MEDIUM_WORD_LENGTH`, `SHORT_WORD_DISTANCE`, `MEDIUM_WORD_DISTANCE`, `LONG_WORD_DISTANCE`
- Ký tự phân tách: `FIELD_SEPARATOR`, `LIST_SEPARATOR`
- Độ dài validation cho từ, nghĩa, ví dụ và lựa chọn menu
- Số lượng field của file dictionary

## Model: Word

`models/Word.py` biểu diễn một mục từ điển.

Hành vi yêu cầu:

- Lưu từ tiếng Anh, nghĩa tiếng Việt, ví dụ và từ đồng nghĩa.
- Không cho thêm từ đồng nghĩa trùng.
- Không cho số lượng từ đồng nghĩa vượt `AppConfig.MAX_SYNONYMS`.
- Chuyển đổi qua lại với dòng file bằng ký tự phân tách đã cấu hình.
- Hiển thị mục từ dễ đọc trong console.

## Cấu Trúc: Trie

`structures/Trie.py` cung cấp tra cứu từ chính xác.

Hành vi yêu cầu:

- Lưu từ tiếng Anh dạng chữ thường.
- Hỗ trợ insert, search và kiểm tra prefix.
- Chỉ xử lý chữ cái tiếng Anh hợp lệ `a-z`.
- Kỳ vọng input đã được normalize trước khi insert/search.

## Cấu Trúc: Dynamic Array

Dự án nên dùng mảng động tự quản lý cho tầng lưu trữ chính của từ điển.

Hành vi yêu cầu:

- Theo dõi dữ liệu nội bộ, size và capacity.
- Hỗ trợ add, get, set, remove, clear, lấy size, kiểm tra rỗng, resize và chuyển sang list.
- Có thể dùng list của Python bên trong, nhưng phải quản lý rõ resize và size.

## Cấu Trúc: History List

History list quản lý các từ được tra cứu gần đây.

Hành vi yêu cầu:

- Thêm từ đã tra cứu.
- Tuân thủ `AppConfig.MAX_HISTORY_SIZE`.
- Xóa phần tử cũ nhất khi danh sách đầy.
- Hỗ trợ display, clear, count, get theo index và chuyển sang list.
- Không crash khi dữ liệu rỗng.

## Cấu Trúc: Favorite List

Favorite list quản lý các từ yêu thích.

Hành vi yêu cầu:

- Hỗ trợ add, remove, kiểm tra tồn tại, display, clear, count, get theo index và chuyển sang list.
- Không cho thêm trùng.
- Chỉ thêm từ đã tồn tại trong từ điển; kiểm tra này thuộc về `DictionaryService`.

## Thuật Toán: Levenshtein

Thuật toán tìm kiếm gần đúng phải được tự cài đặt.

Hành vi yêu cầu:

- Tính edit distance bằng quy hoạch động.
- Trả về `0` với hai chuỗi giống nhau.
- Trả về số thao tác insert/delete/substitute tối thiểu để biến chuỗi này thành chuỗi khác.
- Chọn threshold từ `AppConfig` dựa trên độ dài từ.

## Tiện Ích: String Utils

Các hàm hỗ trợ xử lý chuỗi cần bao gồm:

- Trim
- Chuyển sang chữ thường
- Xóa khoảng trắng dư
- Normalize từ
- Split
- Join

Normalize cần trim, chuyển sang chữ thường và xóa khoảng trắng dư.

## Validation

Validation cần bao phủ:

- Giá trị rỗng
- Khoảng độ dài
- Từ tiếng Anh
- Nghĩa tiếng Việt
- Ví dụ
- Từ đồng nghĩa
- Lựa chọn menu
- Dòng trong file dictionary
- Số lượng field

Validation không được crash với sai kiểu dữ liệu, chuỗi rỗng hoặc `None`.

## File Service

`services/FileService.py` chịu trách nhiệm persistence.

Hành vi yêu cầu:

- Đảm bảo thư mục data tồn tại.
- Load và save các mục dictionary.
- Load và save history.
- Load và save favorites.
- Tạo file thiếu hoặc trả về dữ liệu rỗng.
- Bỏ qua dòng dictionary sai định dạng mà không crash.
- Không chứa logic nghiệp vụ.

## Dictionary Service

`services/DictionaryService.py` chịu trách nhiệm hành vi nghiệp vụ.

Hành vi yêu cầu:

- Load và save toàn bộ dữ liệu.
- Thêm từ.
- Thêm từ đồng nghĩa.
- Tra cứu chính xác.
- Tìm kiếm gần đúng.
- Thêm và xóa favorites.
- Hiển thị history và favorites.
- Hiển thị tất cả từ.
- Kiểm tra từ có tồn tại không.
- Thêm trực tiếp object `Word`.
- Load từ dictionary vào cả dynamic array và trie.
- Thêm lượt tra cứu chính xác thành công vào history.
- Gợi ý tìm kiếm gần đúng khi tra cứu chính xác thất bại.
- Sắp xếp gợi ý gần đúng theo distance và giới hạn bằng `AppConfig.MAX_SUGGESTIONS`.

## UI Menu

`ui/Menu.py` chịu trách nhiệm tương tác console.

Hành vi yêu cầu:

- Hiển thị menu chính.
- Đọc và validate lựa chọn menu.
- Gọi `DictionaryService` cho mọi hành vi.
- Không chứa file I/O và logic nghiệp vụ.
- Lưu dữ liệu trước khi thoát.

## Entrypoint Chính

`main.py` nên cho phép người dùng chạy ứng dụng hoặc test suite. Lựa chọn không hợp lệ nên mặc định chạy ứng dụng.
