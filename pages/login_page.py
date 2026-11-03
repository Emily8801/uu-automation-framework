"""Swag Labs 登录页：元素定位 + 原子操作（断言由 BasePage 提供）。"""

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from core.base_page import BasePage


class LoginPage(BasePage):
    """登录页。"""

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    # 登录成功后进入商品列表页的标志元素
    INVENTORY_CONTAINER = (By.CSS_SELECTOR, "[data-test='inventory-container']")

    def open(self) -> None:
        """打开登录页（地址统一由 config 提供）。"""
        super().open(BASE_URL)

    def fill_username(self, username: str) -> None:
        """输入用户名。"""
        self.input_text(self.USERNAME_INPUT, username)

    def fill_password(self, password: str) -> None:
        """输入密码。"""
        self.input_text(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """点击登录按钮。"""
        self.click(self.LOGIN_BUTTON)
