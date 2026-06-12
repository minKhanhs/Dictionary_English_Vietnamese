# Hướng Dẫn Cho Agent

## Tổng Quan

Repository này là ứng dụng console Python 3 cho từ điển Anh-Việt. Khi chỉnh sửa, hãy giữ mã nguồn rõ module, dễ mở rộng và bám theo tài liệu trong `doc/`.

## Ràng Buộc

- Chỉ dùng thư viện chuẩn của Python.
- Không thêm package bên thứ ba.
- Không dùng thư viện tìm kiếm, fuzzy-search, database, pandas, numpy, pytest hoặc thư viện tương tự.
- Thuật toán và cấu trúc dữ liệu chính phải tiếp tục được tự cài đặt.
- Giữ các giá trị cấu hình trong `config/AppConfig.py`; tránh hard-code đường dẫn, giới hạn và ký tự phân tách.
- Giữ nguyên hành vi console trừ khi yêu cầu thay đổi ảnh hưởng trực tiếp tới luồng UI.

## Quy Tắc Kiến Trúc

- Mã giao diện nằm trong `ui/` và chỉ nên gọi các phương thức service.
- Logic nghiệp vụ nằm trong `services/`.
- Đọc và ghi file nằm trong `services/FileService.py`.
- Model nằm trong `models/`.
- Cấu trúc dữ liệu nằm trong `structures/`.
- Thuật toán nằm trong `algorithms/`.
- Validation nằm trong `validate/`.
- Hàm hỗ trợ xử lý chuỗi nằm trong `utils/`.
- Test nằm trong `tests/`.

## Trước Khi Chỉnh Sửa

- Đọc file liên quan và test gần đó trước.
- Tôn trọng style đặt tên hiện có trong repo, bao gồm các file đang dùng PascalCase.
- Không revert thay đổi của người dùng. Worktree có thể đang có chỉnh sửa không liên quan.
- Giữ cập nhật tài liệu trong `doc/`, trừ khi file đó dành riêng cho agent.

## Kiểm Chứng

- Với thay đổi code, chạy test liên quan bằng test runner của dự án hoặc chọn mục 2 khi chạy `python main.py` nếu phù hợp.
- Với thay đổi chỉ liên quan tài liệu, kiểm tra đường dẫn file và cấu trúc markdown.
