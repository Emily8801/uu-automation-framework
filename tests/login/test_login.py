"""登录功能测试用例：每个 test 方法体只写一行。"""

from core.base_test import BaseTest
from core.step import case_title
from steps.login_steps import LoginSteps


class TestLogin(BaseTest):
    """登录场景：一条用例对应一个数据字典。"""

    data_file = "login_data"

    @case_title("Login succeeds with valid credentials")
    def test_login_success(self):
        LoginSteps(self.driver).login_and_verify(self.data.data_login_success)

    @case_title("Locked-out user cannot log in")
    def test_login_locked(self):
        LoginSteps(self.driver).login_and_verify(self.data.data_login_locked)

    @case_title("Login fails with invalid credentials")
    def test_login_wrong_credentials(self):
        LoginSteps(self.driver).login_and_verify(self.data.data_login_wrong_credentials)

    @case_title("Login fails with empty username")
    def test_login_empty_username(self):
        LoginSteps(self.driver).login_and_verify(self.data.data_login_empty_username)

    @case_title("Login fails with empty password")
    def test_login_empty_password(self):
        LoginSteps(self.driver).login_and_verify(self.data.data_login_empty_password)
