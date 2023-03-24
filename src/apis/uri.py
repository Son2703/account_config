class URI:
    class USER:
        USERS="/users"
        DETAIL="/users/<id_user>"
        CHANGE_PASS = "/users/actions/change-password"
        LOCK = "/users/actions/lock-user"
        BULK_INSERT_MANY = "/users/actions/bulk_insert"
        DELETE ="/users/<id_user>/actions/delete"