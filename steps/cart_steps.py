"""购物车业务步骤。"""

from core.step import step
from pages.inventory_page import InventoryPage
from steps.login_steps import LoginSteps


class CartSteps:
    """购物车流程步骤。"""

    def __init__(self, driver):
        self.login_steps = LoginSteps(driver)
        self.inventory_page = InventoryPage(driver)

    @step
    def add_product_after_login(self, case):
        """Log in and add a product to the cart"""
        self.login_steps.submit_login(case["submit"])
        self.add_product(case["add"])
        self.verify_cart(case["verify"])

    @step
    def add_product(self, data):
        """Click add to cart"""
        self.inventory_page.add_product(data["product"])

    @step
    def verify_cart(self, data):
        """Verify the cart badge count"""
        self.inventory_page.assert_element_text(
            self.inventory_page.CART_BADGE, data["cart_count"]
        )
