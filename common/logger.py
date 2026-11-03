"""统一日志：控制台输出，供步骤装饰器使用。"""

import logging


def get_logger(name: str = "ui_auto") -> logging.Logger:
    """返回带控制台 handler 的 logger（重复调用不会重复添加 handler）。"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", "%H:%M:%S")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
