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

    

LIST_RULE_NAME = [rule.value for rule in list(Rule)]