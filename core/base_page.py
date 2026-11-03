"""页面对象基类：基本动作 + 全部断言。

断言集中在这一层，自带显式等待；失败抛 AssertionError，Allure 报告记为 failed。
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


class BasePage:
    """所有页面对象的基类：等待、原子操作、断言。"""

    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # ---------------- 等待 ----------------
    def _wait_clickable(self, locator: tuple) -> WebElement:
        """等待元素可见且可交互，返回元素本身。"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def _wait_visible(self, locator: tuple) -> WebElement:
        """等待元素可见，返回元素本身。"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _is_displayed(self, locator: tuple) -> bool:
        """等待元素可见后返回展示状态；超时视为不可见。"""
        try:
            return self._wait_visible(locator).is_displayed()
        except TimeoutException:
            return False

    # ---------------- 基本动作 ----------------
    def open(self, url: str) -> None:
        """打开指定地址。"""
        self.driver.get(url)

    def input_text(self, locator: tuple, text: str) -> None:
        """清空后输入文本，避免上一步残留干扰。"""
        element = self._wait_clickable(locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator: tuple) -> None:
        """点击元素（先等可点击）。"""
        self._wait_clickable(locator).click()

    def get_text(self, locator: tuple) -> str:
        """取元素文本，去掉首尾空白。"""
        return self._wait_visible(locator).text.strip()

    def get_current_url(self) -> str:
        """取当前页面地址。"""
        return self.driver.current_url

    def is_visible(self, locator: tuple) -> bool:
        """元素是否可见（不做断言，仅返回结果）。"""
        return self._is_displayed(locator)

    # ---------------- 断言 ----------------
    def assert_url_contains(self, keyword: str) -> None:
        """断言当前 URL 包含指定关键字。"""
        url = self.get_current_url()
        assert keyword in url, f"当前 URL 不含 '{keyword}'，实际为: {url}"

    def assert_element_visible(self, locator: tuple) -> None:
        """断言元素在超时时间内出现。"""
        assert self.is_visible(locator), f"元素在 {self.timeout} 秒内未出现: {locator}"

    def assert_text_contains(self, locator: tuple, expected: str) -> None:
        """断言元素文案包含指定内容。"""
        actual = self.get_text(locator)
        assert expected in actual, f"文案不匹配，期望包含: {expected}，实际: {actual}"

    def assert_element_text(self, locator: tuple, expected: str) -> None:
        """断言元素文案与期望完全相等。"""
        actual = self.get_text(locator)
        assert actual == expected, f"文字不相等，期望: {expected}，实际: {actual}"
