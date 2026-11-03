"""用例基类：开浏览器、加载同级数据、关浏览器。

子类只需声明 data_file（同目录数据模块名），用例体保持一行调用步骤。
"""

import importlib.util
import inspect
from pathlib import Path

import pytest

from common.driver_factory import create_driver


class BaseTest:
    """所有测试类的基类。"""

    data_file = None

    @pytest.fixture(autouse=True)
    def _setup(self, request):
        """每个用例独立开一个浏览器，结束后无条件退出（用例之间互不影响）。"""
        headless = request.config.getoption("--headless")
        self.driver = create_driver(headless=headless)
        if self.data_file:
            self.data = self._load_data(self.data_file)
        yield
        self.driver.quit()

    @classmethod
    def _load_data(cls, name: str):
        """按用例文件所在目录加载数据模块，保证数据与用例同级。"""
        module_path = Path(inspect.getfile(cls)).parent / f"{name}.py"
        spec = importlib.util.spec_from_file_location(
            f"{cls.__module__}.{name}", module_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
