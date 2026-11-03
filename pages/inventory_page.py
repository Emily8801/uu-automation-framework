"""商品列表页：元素定位 + 原子操作（断言由 BasePage 提供）。"""

from selenium.webdriver.common.by import By

from core.base_page import BasePage


class InventoryPage(BasePage):
    """商品列表页（登录成功后自动进入）。"""

    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")

    # 按商品名定位它所在卡片里的按钮（相对 XPath，不使用绝对路径）
    _ADD_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'inventory_item')]"
        "[.//div[normalize-space()='{name}']]//button",
    )

    def add_product(self, product_name: str) -> None:
        """点击指定商品卡片上的加入购物车按钮。"""
        locator = (self._ADD_BUTTON[0], self._ADD_BUTTON[1].format(name=product_name))
        self.click(locator)
