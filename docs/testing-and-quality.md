# Test Và Chất Lượng

## Tổng Quan

Repo hiện dùng `unittest` của Python thay vì test runner tự viết. `main.py` có option chạy test bằng `unittest.TestLoader().discover("tests", pattern="Test*.py")`.

Test suite hiện có 8 file, tổng cộng 147 test case đang pass trong `.venv`.

## Cách Chạy

```bash
.venv/bin/python -m unittest discover -s tests -p 'Test*.py'
.venv/bin/basedpyright
.venv/bin/ruff check .
```

Nếu dùng `main.py`:

```bash
.venv/bin/python main.py
```

Sau đó chọn `2. Chạy unit test`.

## Trạng Thái Gần Nhất

| Kiểm tra | Lệnh | Kết quả |
| --- | --- | --- |
| Unit test | `.venv/bin/python -m unittest discover -s tests -p 'Test*.py'` | Pass: 147 tests |
| Type check | `.venv/bin/basedpyright` | Pass: 0 errors |
| Lint | `.venv/bin/ruff check .` | Fail: 14 issues |

`python`, `ruff` không có trong PATH của shell hiện tại; dùng binary trong `.venv/bin/`.

## Phạm Vi Test Hiện Có

| File | Phạm vi |
| --- | --- |
| `tests/TestArrayList.py` | `ArrayList`, resize, remove, bounds, alias `DynamicArray` |
| `tests/TestTrie.py` | `Trie`, `startsWith`, invalid char, word data |
| `tests/TestFuzzySearch.py` | `Levenshtein`, `FuzzySearch`, max distance, max suggestions |
| `tests/TestWord.py` | `models.Word`, meaning merge, synonyms, file roundtrip |
| `tests/TestValidation.py` | Input validation, menu option, dictionary line |
| `tests/TestHistoryList.py` | Normalize, FIFO eviction, clear, toList |
| `tests/TestFavoriteList.py` | Add/remove/contains, duplicate, normalize |
| `tests/TestDictionaryService.py` | CRUD, import merge, search, history, favorites, delete |

## Test Case Quan Trọng

| Phạm vi | Hành vi đang được kiểm tra |
| --- | --- |
| Tạo từ | Normalize english, giữ nghĩa/ví dụ/synonyms |
| Từ trùng | `addWordObject()` từ chối duplicate |
| Import duplicate | `importWordObject()` merge nghĩa và synonym |
| Search exact | Tìm thấy trả `Word`, miss trả `None` |
| History | Chỉ search exact thành công mới ghi history |
| Search approximate | Gợi ý từ typo, giới hạn bằng `MAX_SUGGESTIONS` |
| Delete word | Xóa khỏi `ArrayList`, rebuild Trie, xóa khỏi favorites |
| Trie | Chỉ nhận `a-z`, reject dấu cách và dấu gạch ngang |
| Validation | English word hiện cho phép chữ, dấu cách và dấu gạch ngang |
| Favorites | Chống duplicate và normalize case |

## Quality Gates

### Unit Test

Unit test đang là quality gate đáng tin cậy nhất ở thời điểm hiện tại:

```text
Ran 147 tests
OK
```

Một số test in log từ app như `[EMPTY]` hoặc `[FAIL] isValidMenuOption...`; đây là side effect của code production, không phải test failure.

### Type Check

`basedpyright` đang pass:

```text
0 errors, 0 warnings, 0 notes
```

`pyproject.toml` cấu hình `pythonVersion = "3.14"` và `typeCheckingMode = "basic"`.

### Lint

`ruff check .` hiện fail 14 issues:

- Line length > 88 trong `models/Word.py`, `structures/Word.py`, `ui/Menu.py`, `ui/MenuHandler.py`.
- Unused import `Word` trong `services/DictionaryService.py`.
- Deprecated `typing.List` và import ordering trong `utils/StringUtils.py`.

Ruff chưa nên được ghi là pass cho đến khi các lỗi này được sửa.

## Coverage Gaps

Các điểm nên bổ sung test nếu tiếp tục phát triển:

| Gap | Lý do |
| --- | --- |
| `FileService` với file thiếu, file invalid, save failure | Docs cũ yêu cầu nhưng test hiện chưa có file service riêng |
| `structures.Word` trực tiếp | Runtime dùng `structures.Word`, nhưng `TestWord` đang test `models.Word` |
| Từ có dấu cách hoặc dấu gạch ngang qua `DictionaryService.addWordObject()` | Đây là mismatch giữa Validation và Trie |
| Menu handler | Chưa có test với mocked `input()`/service |
| `main.runTests()` và `main.runApplication()` | Chưa có test entrypoint |

## Known Conflicts Giữa Quality Và Code

| Conflict | Hiện trạng | Lựa chọn cần quyết định |
| --- | --- | --- |
| Validation vs Trie | Validation cho phép `hello-world`, Trie reject | Sửa validation hoặc mở rộng Trie |
| Hai implementation `Word` | Tests dùng `models.Word`, runtime dùng `structures.Word` | Hợp nhất class hoặc test cả hai |
| Ruff fail | Không ảnh hưởng unit test/typecheck hiện tại | Sửa style hoặc bỏ Ruff khỏi gate bắt buộc |

## Khuyến Nghị Ngắn

Nếu mục tiêu tiếp theo là làm codebase sạch hơn, ưu tiên:

1. Quyết định rule ký tự cho English word rồi sửa validation/Trie/service tương ứng.
2. Hợp nhất `models.Word` và `structures.Word`.
3. Sửa Ruff để lint trở thành quality gate pass.
4. Thêm test cho `FileService` và mismatch validation/Trie.
