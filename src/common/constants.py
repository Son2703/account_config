from enum import Enum

class TimeConfig(Enum):
    UTC_ZONE = "UTC"

class Rule(Enum):
    VAL_NAME = "val_name"
    VAL_PASS = "val_pass"
    CHANGE_PASS_MOTH = "change_pass_moth"
    UNIQUE_OLD_PASS = "unique_old_pass"
    REQUIRE_CHANGE_PASS = "require_change_pass"
    UNIQUE_PASS = "unique_pass"
    LOCK_ACCOUNT = "lock_account"

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class DatabaseName(Enum):
    COL_RULE = "rules"
    COL_USER = "users"
    COL_LIST_PASS_USER = "list_pass_users"
    COL_MERCHANT_RULE_ASSIGNMENT = "merchant_rule_assignments"
    COL_MERCHANT = "merchants"