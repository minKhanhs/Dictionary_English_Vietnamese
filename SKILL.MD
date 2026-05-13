Bạn là Codex, hãy viết một chương trình từ điển Anh–Việt bằng Python theo yêu cầu dưới đây.

Mục tiêu:
Xây dựng chương trình console cho phép người dùng quản lý và tra cứu từ điển Anh–Việt. Chương trình phải được chia module rõ ràng, dễ mở rộng, có validation, có config tránh hard-code, có unit test và test case.

Ngôn ngữ:
Python 3.

Không dùng thư viện ngoài.
Chỉ được dùng thư viện chuẩn của Python.
Không dùng các thư viện tìm kiếm, fuzzy search, database, pandas, numpy hoặc thư viện test ngoài như pytest.
Các thuật toán chính phải tự cài đặt.

Yêu cầu chức năng:
1. Người dùng có thể thêm từ mới.
2. Người dùng có thể thêm nghĩa tiếng Việt cho từ tiếng Anh.
3. Người dùng có thể thêm ví dụ sử dụng.
4. Người dùng có thể thêm từ đồng nghĩa.
5. Người dùng có thể tra cứu chính xác từ tiếng Anh.
6. Nếu không tìm thấy chính xác, chương trình có thể gợi ý các từ gần giống.
7. Tìm kiếm gần đúng sử dụng thuật toán Levenshtein Distance tự cài đặt.
8. Chương trình lưu lịch sử các từ đã tra cứu gần đây.
9. Chương trình cho phép đánh dấu từ yêu thích, gọi là Favorites.
10. Chương trình đọc và ghi dữ liệu bằng file text.
11. Người dùng thao tác bằng menu console cho đến khi chọn thoát.
12. Chương trình cần có validation đầu vào và lập trình phòng ngừa.
13. Chương trình cần có unit test tự viết, không dùng pytest hoặc unittest nếu không cần thiết. Ưu tiên tự viết TestRunner đơn giản.

Cấu trúc thư mục bắt buộc:

DictionaryProject/
│
├── main.py
│
├── config/
│   ├── __init__.py
│   └── app_config.py
│
├── models/
│   ├── __init__.py
│   └── word.py
│
├── structures/
│   ├── __init__.py
│   ├── trie.py
│   ├── dynamic_array.py
│   ├── history_list.py
│   └── favorite_list.py
│
├── algorithms/
│   ├── __init__.py
│   └── levenshtein.py
│
├── services/
│   ├── __init__.py
│   ├── dictionary_service.py
│   └── file_service.py
│
├── validation/
│   ├── __init__.py
│   └── validator.py
│
├── utils/
│   ├── __init__.py
│   └── string_utils.py
│
├── ui/
│   ├── __init__.py
│   └── menu.py
│
├── tests/
│   ├── __init__.py
│   ├── test_runner.py
│   ├── all_tests.py
│   ├── word_test.py
│   ├── trie_test.py
│   ├── levenshtein_test.py
│   ├── validator_test.py
│   ├── dynamic_array_test.py
│   ├── history_list_test.py
│   └── favorite_list_test.py
│
└── data/
    ├── dictionary.txt
    ├── history.txt
    └── favorites.txt

Vai trò từng module:

1. config/app_config.py
Chứa toàn bộ cấu hình chương trình, tránh hard-code.

Cần có class AppConfig với các biến:
- DATA_FOLDER
- DICTIONARY_FILE
- HISTORY_FILE
- FAVORITES_FILE
- MAX_SYNONYMS
- MAX_HISTORY_SIZE
- MAX_SUGGESTIONS
- ALPHABET_SIZE
- FIRST_CHAR
- LAST_CHAR
- SHORT_WORD_LENGTH
- MEDIUM_WORD_LENGTH
- SHORT_WORD_DISTANCE
- MEDIUM_WORD_DISTANCE
- LONG_WORD_DISTANCE
- FIELD_SEPARATOR
- LIST_SEPARATOR
- MIN_WORD_LENGTH
- MAX_WORD_LENGTH
- MIN_MEANING_LENGTH
- MAX_MEANING_LENGTH
- MIN_EXAMPLE_LENGTH
- MAX_EXAMPLE_LENGTH
- MIN_MENU_OPTION
- MAX_MENU_OPTION
- DICTIONARY_FILE_FIELD_COUNT

Ví dụ:
DATA_FOLDER = "data/"
DICTIONARY_FILE = "data/dictionary.txt"
HISTORY_FILE = "data/history.txt"
FAVORITES_FILE = "data/favorites.txt"
MAX_SYNONYMS = 10
MAX_HISTORY_SIZE = 20
MAX_SUGGESTIONS = 5
FIELD_SEPARATOR = "|"
LIST_SEPARATOR = ","

2. models/word.py
Tạo class Word.

Thuộc tính:
- english
- vietnamese
- example
- synonyms

Phương thức:
- get_english()
- get_vietnamese()
- get_example()
- get_synonyms()
- get_synonym_count()
- set_english()
- set_vietnamese()
- set_example()
- add_synonym()
- has_synonym()
- display()
- to_file_line()
- from_file_line()

Lưu ý:
- Không cho thêm synonym trùng.
- Không cho số lượng synonym vượt AppConfig.MAX_SYNONYMS.
- to_file_line dùng FIELD_SEPARATOR và LIST_SEPARATOR từ AppConfig.

3. structures/trie.py
Tự cài đặt Trie để tìm kiếm chính xác.

Tạo class TrieNode:
- children
- is_end_of_word
- word_data

Tạo class Trie:
- root
- insert(word)
- search(english)
- starts_with(prefix)
- _get_index(char)
- _is_valid_char(char)

Trie chỉ xử lý các chữ cái tiếng Anh a-z.
Input nên được normalize trước khi insert/search.

4. structures/dynamic_array.py
Tự cài đặt mảng động thay cho list thông thường ở tầng lưu trữ chính.

Tạo class DynamicArray:
- data
- size
- capacity

Phương thức:
- push_back(item)
- get(index)
- set(index, item)
- remove_at(index)
- get_size()
- is_empty()
- clear()
- _resize()
- to_list()

Không dùng list như cấu trúc chính một cách trực tiếp cho nghiệp vụ từ điển, mà dùng DynamicArray để thể hiện tự cài đặt cấu trúc dữ liệu.
Có thể dùng list nội bộ để mô phỏng mảng động, nhưng phải tự quản lý size, capacity và resize.

5. structures/history_list.py
Quản lý lịch sử tra cứu gần đây.

Class HistoryList:
- items
- count

Phương thức:
- add(word)
- display()
- get_count()
- get_item(index)
- clear()
- to_list()

Yêu cầu:
- Giới hạn số lượng bằng AppConfig.MAX_HISTORY_SIZE.
- Nếu đầy thì xóa phần tử cũ nhất.
- Không crash khi danh sách rỗng.

6. structures/favorite_list.py
Quản lý danh sách từ yêu thích.

Class FavoriteList:
- favorites

Phương thức:
- add(word)
- remove(word)
- contains(word)
- display()
- get_count()
- get_item(index)
- clear()
- to_list()

Yêu cầu:
- Không cho thêm trùng.
- Chỉ thêm từ đã tồn tại trong từ điển, phần kiểm tra này đặt trong DictionaryService.

7. algorithms/levenshtein.py
Tự cài đặt thuật toán Levenshtein Distance.

Class Levenshtein:
- distance(a, b)
- get_threshold(word_length)

distance(a, b):
- Dùng quy hoạch động.
- Không dùng thư viện ngoài.
- Trả về số thao tác ít nhất để biến chuỗi a thành chuỗi b.

get_threshold(word_length):
- Nếu độ dài <= SHORT_WORD_LENGTH, trả về SHORT_WORD_DISTANCE.
- Nếu độ dài <= MEDIUM_WORD_LENGTH, trả về MEDIUM_WORD_DISTANCE.
- Ngược lại trả về LONG_WORD_DISTANCE.

8. utils/string_utils.py
Chứa các hàm xử lý chuỗi.

Class StringUtils:
- trim(value)
- to_lower_case(value)
- remove_extra_spaces(value)
- normalize_word(value)
- split(value, separator)
- join(items, separator)

normalize_word:
- trim
- chuyển thành chữ thường
- loại bỏ khoảng trắng dư thừa

9. validation/validator.py
Chứa toàn bộ validation.

Class Validator:
- is_empty(value)
- is_length_in_range(value, min_length, max_length)
- is_valid_english_word(word)
- is_valid_vietnamese_meaning(meaning)
- is_valid_example(example)
- is_valid_synonym(synonym)
- is_valid_menu_choice(choice, min_choice, max_choice)
- is_valid_dictionary_line(line)
- has_enough_fields(line, separator, expected_fields)

Yêu cầu validation:
- English word không được rỗng.
- English word chỉ gồm chữ cái a-z, khoảng trắng hoặc dấu gạch ngang.
- Vietnamese meaning không được rỗng.
- Menu choice phải nằm trong khoảng hợp lệ.
- Dòng file dictionary phải có đủ field.
- Không crash nếu input sai kiểu, chuỗi rỗng hoặc None.

10. services/file_service.py
Chịu trách nhiệm đọc/ghi file.

Class FileService:
- ensure_data_folder()
- load_dictionary()
- save_dictionary(words)
- load_history()
- save_history(history)
- load_favorites()
- save_favorites(favorites)

Yêu cầu:
- Nếu file không tồn tại thì tạo file hoặc trả về dữ liệu rỗng.
- Nếu dòng dữ liệu sai định dạng thì bỏ qua, không crash.
- Không xử lý nghiệp vụ trong FileService.
- FileService chỉ đọc/ghi và parse dữ liệu.

Định dạng dictionary.txt:
english|vietnamese|example|synonym1,synonym2,synonym3

Ví dụ:
hello|xin chào|Hello, how are you?|hi,hey
student|học sinh, sinh viên|He is a student.|pupil,learner

Định dạng history.txt:
Mỗi dòng là một từ đã tra cứu.

Định dạng favorites.txt:
Mỗi dòng là một từ yêu thích.

11. services/dictionary_service.py
Xử lý nghiệp vụ chính.

Class DictionaryService:
Thuộc tính:
- trie
- words
- history
- favorites
- file_service

Phương thức:
- load_data()
- save_data()
- add_word_interactive()
- add_synonym_interactive()
- search_exact_interactive()
- search_approximate_interactive()
- search_exact(word)
- search_approximate(word)
- add_favorite_interactive()
- remove_favorite_interactive()
- show_history()
- show_favorites()
- display_all_words()
- word_exists(word)
- add_word_object(word)

Yêu cầu:
- Khi load dictionary, phải thêm word vào DynamicArray và Trie.
- Khi thêm từ mới, phải validate.
- Không cho thêm từ trùng.
- Khi search exact thành công, phải thêm vào history.
- Khi search exact thất bại, gợi ý tìm kiếm gần đúng.
- Khi thêm favorite, chỉ cho phép thêm từ tồn tại trong từ điển.
- search_approximate duyệt qua DynamicArray, tính Levenshtein với từng từ.
- Chỉ hiển thị tối đa AppConfig.MAX_SUGGESTIONS gợi ý tốt nhất.
- Gợi ý nên được sắp theo distance tăng dần.

12. ui/menu.py
Chứa giao diện menu console.

Class Menu:
- dictionary_service
- show_main_menu()
- input_choice()
- run()

Menu cần có các lựa chọn:
1. Thêm từ mới
2. Thêm từ đồng nghĩa
3. Tra cứu chính xác
4. Tìm kiếm gần đúng
5. Hiển thị lịch sử tra cứu
6. Thêm từ vào Favorites
7. Xóa từ khỏi Favorites
8. Hiển thị Favorites
9. Hiển thị tất cả từ
10. Lưu dữ liệu
0. Thoát

Yêu cầu:
- input_choice phải xử lý nhập sai kiểu, ví dụ người dùng nhập chữ.
- Khi thoát chương trình, gọi save_data().
- Menu chỉ gọi DictionaryService, không xử lý thuật toán, không đọc ghi file trực tiếp.

13. main.py
Chạy chương trình.

Khi chạy, hiển thị:
1. Run application
2. Run unit tests

Nếu chọn 1:
- Tạo Menu và chạy chương trình.

Nếu chọn 2:
- Chạy AllTests.run_all()

Nếu nhập sai:
- Mặc định chạy application.

14. tests/test_runner.py
Tự viết TestRunner đơn giản.

Class TestRunner:
- total_tests
- passed_tests
- failed_tests
- assert_true(condition, test_name)
- assert_false(condition, test_name)
- assert_equal(expected, actual, test_name)
- print_summary()

Không dùng pytest.
Không dùng unittest nếu không cần thiết.

15. tests
Viết test cho các module:
- WordTest
- TrieTest
- LevenshteinTest
- ValidatorTest
- DynamicArrayTest
- HistoryListTest
- FavoriteListTest

Mỗi file test có class tương ứng và hàm static run(runner).

Ví dụ:
class LevenshteinTest:
    @staticmethod
    def run(runner):
        runner.assert_equal(0, Levenshtein.distance("hello", "hello"), "same word distance should be 0")
        runner.assert_equal(1, Levenshtein.distance("helo", "hello"), "one insertion")
        runner.assert_equal(1, Levenshtein.distance("cat", "cut"), "one substitution")
        runner.assert_equal(3, Levenshtein.distance("kitten", "sitting"), "kitten sitting should be 3")

16. tests/all_tests.py
Chạy toàn bộ test.

Class AllTests:
- run_all()

Trong run_all:
- Tạo TestRunner.
- Gọi WordTest.run(runner)
- Gọi TrieTest.run(runner)
- Gọi LevenshteinTest.run(runner)
- Gọi ValidatorTest.run(runner)
- Gọi DynamicArrayTest.run(runner)
- Gọi HistoryListTest.run(runner)
- Gọi FavoriteListTest.run(runner)
- In summary.

17. Test case cần đảm bảo:
- Thêm từ mới thành công.
- Không thêm từ trùng.
- Không thêm từ rỗng.
- Không thêm từ có số.
- Thêm synonym thành công.
- Không thêm synonym trùng.
- Trie tìm được từ đã insert.
- Trie trả về None nếu không tìm thấy.
- Levenshtein trả về 0 với hai chuỗi giống nhau.
- Levenshtein trả về 1 khi thêm/xóa/thay một ký tự.
- Levenshtein("kitten", "sitting") trả về 3.
- HistoryList thêm và giới hạn đúng số lượng.
- FavoriteList không cho thêm trùng.
- Validator bắt lỗi input không hợp lệ.
- FileService không crash khi file không tồn tại hoặc dòng sai format.

18. Yêu cầu code style:
- Code rõ ràng, dễ đọc.
- Mỗi class đặt trong file riêng theo đúng module.
- Tên class dùng PascalCase.
- Tên hàm và biến dùng snake_case.
- Có docstring ngắn cho các class quan trọng.
- Có xử lý ngoại lệ cơ bản khi đọc/ghi file.
- Không để logic nghiệp vụ trong UI.
- Không để đọc/ghi file trong Menu.
- Không hard-code đường dẫn file, số lượng max, separator. Tất cả lấy từ AppConfig.

19. Yêu cầu đầu ra:
Hãy tạo đầy đủ toàn bộ file code theo cấu trúc thư mục trên.
Sau khi tạo code, giải thích ngắn gọn:
- Cách chạy chương trình.
- Cách chạy unit test.
- Vai trò các module.
- Một vài test case chính.