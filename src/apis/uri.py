class URI:
    class RULE:
        RULES="/rules"
        RULE_DETAIL="/rule/<rule_id>"
        RULE_DISABLE_ONE_RULE="/rule/<rule_id>/action/disable"
        RULE_ACTIVE_ONE_RULE="/rule/<rule_id>/action/active"
        RULE_DISABLE_LIST_RULE="/rules/action/disable"

    class USER:
        USERS="/users"
        USER_DETAIL="/user/<user_id>"
        USER_CHANGEPASS = "/user/<user_id>/actions/change-password"
        USER_LOCK = "/user/actions/lock-user"
        USER_BULK_INSERT_MANY = "/users/actions/bulk_insert"
        USER_DELETE ="/user/<user_id>/actions/delete"
        USER_BULK_INSERT_MANY_EXCEL = "/users/actions/import_excel"

    