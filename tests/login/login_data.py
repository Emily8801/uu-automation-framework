"""登录场景测试数据：每个场景一个独立字典，key 与步骤名对应。"""

data_login_success = {
    "submit": {"username": "standard_user", "password": "secret_sauce"},
    "verify": {"success": True, "error": None},
}

data_login_locked = {
    "submit": {"username": "locked_out_user", "password": "secret_sauce"},
    "verify": {"success": False, "error": "Sorry, this user has been locked out"},
}

data_login_wrong_credentials = {
    "submit": {"username": "wrong_user", "password": "wrong_pass"},
    "verify": {"success": False, "error": "Username and password do not match"},
}

data_login_empty_username = {
    "submit": {"username": "", "password": "secret_sauce"},
    "verify": {"success": False, "error": "Username is required"},
}

data_login_empty_password = {
    "submit": {"username": "standard_user", "password": ""},
    "verify": {"success": False, "error": "Password is required"},
}
