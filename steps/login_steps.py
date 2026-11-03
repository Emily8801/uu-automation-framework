"""登录业务步骤。"""

from core.step import step
from pages.login_page import LoginPage


class LoginSteps:
    """登录流程步骤。"""

    def __init__(self, driver):
        self.login_page = LoginPage(driver)

    @step
    def login_and_verify(self, case):
        """登录并校验结果"""
        self.submit_login(case["submit"])
        self.verify_result(case["verify"])

    @step
    def submit_login(self, data):
        """提交账号密码"""
        self.login_page.open()
        self.login_page.fill_username(data["username"])
        self.login_page.fill_password(data["password"])
        self.login_page.click_login()

    @step
    def verify_result(self, data):
        """校验登录结果"""
        if data["success"]:
            # 先等首页元素出现(显式等待兜底跳转)，再断言 URL，避免竞态
            self.login_page.assert_element_visible(self.login_page.INVENTORY_CONTAINER)
            self.login_page.assert_url_contains("inventory")
        else:
            self.login_page.assert_text_contains(
                self.login_page.ERROR_MESSAGE, data["error"]
            )
