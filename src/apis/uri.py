class URI:
    class RULE:
        RULES="/rules"
        RULE_DETAIL="/rule/<rule_id>"
        RULE_DISABLE_ONE_RULE="/rule/<rule_id>/action/disable"
        RULE_ACTIVE_ONE_RULE="/rule/<rule_id>/action/active"
        RULE_DISABLE_LIST_RULE="/rules/action/disable"

    class USER:
        USERS="/users"
        USER_INSERT_MANY_EXCEL = "/users/actions/import_excel"
        
        DETAIL="/users/<id_user>"
        CHANGE_PASS = "/users/actions/change-password"
        LOCK = "/users/actions/lock-user"
        BULK_INSERT_MANY = "/users/actions/bulk_insert"
        DELETE ="/users/<id_user>/actions/delete"
        
