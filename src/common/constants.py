from enum import Enum

class Rule(Enum):
    VAL_NAME = "val_name"
    VAL_PASS = "val_pass"
    CHANGE_PASS_MOTH = "change_pass_moth" # thay đổi theo tháng
    UNIQUE_OLD_PASS = "unique_old_pass" # không trùng pass cũ
    REQUIRE_CHANGE_PASS = "require_change_pass" # thay đổi lần đầu đăng nhập
    UNIQUE_PASS = "unique_pass" # mật khẩu không trùng
    LOCK_ACCOUNT = "lock_account"

    

LIST_RULE_NAME = [rule.value for rule in list(Rule)]
class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class DatabaseName(Enum):
    COL_RULE = "rules"
    COL_USER = "users"
    COL_LIST_PASS_USER = "list_pass_users"
    COL_MERCHANT_RULE_ASSIGNMENT = "merchant_rule_assignments"
    COL_MERCHANT = "merchants"

class Status(Enum):
    ACTIVATE = 1
    DEACTIVATE = 2
    DELETE = 3

class TimeChoise(Enum):
    ONE_HOUR = 1
