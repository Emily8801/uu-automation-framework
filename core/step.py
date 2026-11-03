"""报告装饰器：@step 记录步骤树，@case_title 设置用例标题。"""

import functools
import inspect

import allure

from common.logger import get_logger

logger = get_logger("step")

# 参数名命中这些关键字时，报告里不记录明文
SENSITIVE_KEYS = ("password", "pwd", "passwd", "token", "secret")


def _mask(key: str, value):
    """密码类参数只记录长度，不记录明文。"""
    if any(k in key.lower() for k in SENSITIVE_KEYS) and value:
        return f"****({len(str(value))})"
    return value


def _attach_params(func, args, kwargs) -> None:
    """把方法入参作为附件写进当前步骤；字典参数递归展开，逐字段记录。"""
    signature = inspect.signature(func)
    # 跳过 self
    bound = signature.bind_partial(*args[1:], **kwargs)

    for key, value in bound.arguments.items():
        _attach_value(str(key), value)


def _attach_value(key: str, value) -> None:
    """递归处理嵌套字典，保证最内层的密码字段也能脱敏。"""
    if isinstance(value, dict):
        for item_key, item_value in value.items():
            _attach_value(str(item_key), item_value)
        return

    allure.attach(
        str(_mask(key, value)),
        name=key,
        attachment_type=allure.attachment_type.TEXT,
    )


def step(func):
    """把步骤方法变成报告里的一层步骤，同时输出控制台日志。"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        title = (inspect.getdoc(func) or func.__name__).strip().splitlines()[0]
        logger.info("▶ %s", title)
        with allure.step(title):
            _attach_params(func, args, kwargs)
            result = func(*args, **kwargs)
        logger.info("✔ %s", title)
        return result

    return wrapper


def case_title(title: str):
    """给用例设置报告显示名（中文标题），不影响 pytest 的用例 ID。"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            allure.dynamic.title(title)
            return func(*args, **kwargs)

        return wrapper

    return decorator
