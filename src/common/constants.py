from enum import Enum

class TimeConfig(Enum):
    UTC_ZONE = "UTC"

class Rule(Enum):
    VAL_NAME = "val_name"
    VAL_PASS = "val_pass"
    CHANGE_PASS_MOTH = "change_pass_moth" # thay đổi theo tháng
    UNIQUE_OLD_PASS = "unique_old_pass" # không trùng pass cũ
    REQUIRE_CHANGE_PASS = "require_change_pass" # thay đổi lần đầu đăng nhập
    UNIQUE_PASS = "unique_pass" # mật khẩu không trùng
    LOCK_ACCOUNT = "lock_account"

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class Status(Enum):
    ACTIVATE = 1
    DEACTIVE = 2

