# Yêu Cầu Dự Án

## Tổng Quan

Xây dựng ứng dụng console bằng Python 3 cho phép người dùng quản lý và tra cứu từ điển Anh-Việt. Chương trình cần được chia module rõ ràng, dễ mở rộng, có validation, có cấu hình tránh hard-code và có test.

## Ràng Buộc

- Dùng Python 3.
- Chỉ dùng thư viện chuẩn.
- Không dùng thư viện fuzzy-search, database, pandas, numpy, pytest hoặc thư viện tương tự.
- Tự cài đặt các thuật toán chính.
- Đọc và ghi dữ liệu bằng file text.

## Chức Năng

1. Thêm từ tiếng Anh mới.
2. Thêm nghĩa tiếng Việt cho từ tiếng Anh.
3. Thêm ví dụ sử dụng.
4. Thêm từ đồng nghĩa.
5. Tra cứu chính xác từ tiếng Anh.
6. Gợi ý từ gần giống khi không tìm thấy kết quả chính xác.
7. Dùng thuật toán Levenshtein Distance tự cài đặt cho tìm kiếm gần đúng.
8. Lưu lịch sử tra cứu gần đây.
9. Đánh dấu từ yêu thích.
10. Đọc và ghi dữ liệu từ điển bằng file text.
11. Giữ menu console chạy cho đến khi người dùng chọn thoát.
12. Validate input và lập trình phòng ngừa.
13. Cung cấp unit test tự viết hoặc test runner đơn giản.

## File Dữ Liệu

Các file dữ liệu kỳ vọng:

```text
data/dictionary.txt
data/history.txt
data/favorites.txt
```

Repository hiện tại cũng đang có một số file text runtime ở thư mục root. Ưu tiên dùng đường dẫn được cấu hình trong `AppConfig` thay vì hard-code.

## Định Dạng Dictionary

Mỗi dòng dictionary dùng định dạng:

```text
english|vietnamese|example|synonym1,synonym2,synonym3
```

Ví dụ:

```text
hello|xin chào|Hello, how are you?|hi,hey
student|học sinh, sinh viên|He is a student.|pupil,learner
```

## Định Dạng History

Mỗi dòng trong `history.txt` là một từ đã được tra cứu.

## Định Dạng Favorites

Mỗi dòng trong `favorites.txt` là một từ yêu thích.

## Luồng Console

Khi chạy `main.py`, hiển thị:

```text
1. Run application
2. Run unit tests
```

Nếu người dùng chọn chế độ ứng dụng, tạo và chạy menu. Nếu người dùng chọn test, chạy toàn bộ test. Input không hợp lệ nên mặc định chạy ứng dụng.

## Tùy Chọn Menu

Menu cần hỗ trợ:

| Lựa chọn | Hành động |
| --- | --- |
| 1 | Thêm từ mới |
| 2 | Thêm từ đồng nghĩa |
| 3 | Tra cứu chính xác |
| 4 | Tìm kiếm gần đúng |
| 5 | Hiển thị lịch sử tra cứu |
| 6 | Thêm vào Favorites |
| 7 | Xóa khỏi Favorites |
| 8 | Hiển thị Favorites |
| 9 | Hiển thị tất cả từ |
| 10 | Lưu dữ liệu |
| 0 | Thoát |

Khi thoát, gọi luồng lưu dữ liệu.
