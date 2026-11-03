"""购物车功能测试用例：每个 test 方法体只写一行。"""

from core.base_test import BaseTest
from core.step import case_title
from steps.cart_steps import CartSteps


class TestAddToCart(BaseTest):
    """购物车场景：一条用例对应一个数据字典。"""

    data_file = "cart_data"

    @case_title("登录后添加背包到购物车")
    def test_add_backpack(self):
        CartSteps(self.driver).add_product_after_login(self.data.data_add_backpack)
