# Test Và Chất Lượng

## Test Runner

Yêu cầu ban đầu đề xuất một test runner đơn giản với:

- `total_tests`
- `passed_tests`
- `failed_tests`
- `assert_true(condition, test_name)`
- `assert_false(condition, test_name)`
- `assert_equal(expected, actual, test_name)`
- `print_summary()`

Repository hiện tại đang dùng `unittest` của Python. Hãy giữ các test hiện có hoạt động, trừ khi task yêu cầu thay đổi cách test rõ ràng.

## Phạm Vi Test Yêu Cầu

Test nên bao phủ:

- `Word`
- `Trie`
- Levenshtein hoặc hành vi fuzzy search
- Validation
- Dynamic array / array list
- History list
- Favorite list
- Hành vi dictionary service
- Hành vi file service khi thiếu file hoặc có dòng sai định dạng

## Test Case Chính

| Phạm vi | Trường hợp kỳ vọng |
| --- | --- |
| Tạo từ | Thêm từ mới thành công |
| Từ trùng | Từ chối từ bị trùng |
| Validation | Từ chối từ rỗng |
| Validation | Từ chối từ chứa số |
| Từ đồng nghĩa | Thêm từ đồng nghĩa thành công |
| Từ đồng nghĩa | Từ chối từ đồng nghĩa bị trùng |
| Trie | Tìm được từ đã insert |
| Trie | Trả về không tìm thấy với từ không tồn tại |
| Levenshtein | Distance là `0` với hai chuỗi giống nhau |
| Levenshtein | Distance là `1` với một thao tác insert/delete/substitute |
| Levenshtein | `kitten` sang `sitting` trả về `3` |
| History | Tuân thủ kích thước history tối đa |
| Favorites | Từ chối favorite bị trùng |
| File service | Không crash khi thiếu file |
| File service | Bỏ qua dòng dictionary sai định dạng |

## Code Style

- Giữ code rõ ràng và dễ đọc.
- Đặt mỗi class quan trọng trong một file riêng.
- Dùng PascalCase cho tên class.
- Dùng snake_case cho method và biến khi tạo API Python mới, trừ khi cần khớp với style hiện tại của repo.
- Thêm docstring ngắn cho các class quan trọng.
- Xử lý exception cơ bản khi đọc/ghi file.
- Không để logic nghiệp vụ trong file UI.
- Không để logic đọc/ghi file trong file menu.
- Không hard-code đường dẫn, số lượng tối đa hoặc ký tự phân tách.

## Ghi Chú Đầu Ra Kỳ Vọng

Sau khi tạo code hoặc cập nhật lớn, cần ghi lại:

- Cách chạy ứng dụng.
- Cách chạy test.
- Vai trò của từng module.
- Một vài test case quan trọng.
