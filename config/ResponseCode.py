"""Central status codes for the application and test suites."""


class ResponseCode:
    """Standard status codes used when reporting app and test responses."""

    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"

    PASS_LABEL = f"[{PASS}]"
    FAIL_LABEL = f"[{FAIL}]"
    SKIP_LABEL = f"[{SKIP}]"

    # Mã Lỗi / Trạng Thái Ứng Dụng (Application Codes)
    SUCCESS = "S"          # Thành công
    INFO = "INFO"          # Thông tin chung
    INPUT_INVALID = "IV"   # Lỗi dữ liệu đầu vào
    NOT_FOUND = "NF"       # Không tìm thấy dữ liệu
    DUPLICATE = "DUP"      # Dữ liệu bị trùng lặp
    FILE_ERROR = "IO"      # Lỗi đọc/ghi file
    EMPTY = "EMPTY"        # Dữ liệu trống
    CANCELLED = "CANCEL"   # Người dùng hủy thao tác
    ERROR = "ERR"          # Lỗi chung chung hoặc không xác định
