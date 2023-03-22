class URI:
    class USER:
        USERS="/users"
        USER_DETAIL="/user/<user_id>"
        USER_CHANGEPASS = "/user/<user_id>/actions/change-password"
        USER_LOCK = "/user/actions/lock-user"
        USER_BULK_INSERT_MANY = "/users/actions/bulk_insert"
        USER_DELETE ="/user/<user_id>/actions/delete"