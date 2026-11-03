"""全局钩子：--headless 参数、失败截图、邮件报告、执行阶段异常统一转 failed。"""

import allure
import pytest


def pytest_addoption(parser):
    """注册 --headless 和 --send-mail 命令行参数。"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="以无头模式运行 Chrome（CI / 无显示器环境建议开启）",
    )
    parser.addoption(
        "--send-mail",
        action="store_true",
        default=False,
        help="测试结束后把 Allure 报告发送到邮箱（相同结果会自动跳过，避免重复邮件）",
    )


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item):
    """执行阶段的非断言异常统一转成 AssertionError，报告里只出现 failed。

    用 hookwrapper 包装而不是直接调 item.runtest()，否则会和 pytest 默认实现
    重复执行用例（每个用例跑两遍）。
    """
    outcome = yield
    excinfo = outcome.excinfo
    if excinfo is None:
        return

    exc_type, exc, _ = excinfo
    # 断言失败 / pytest.fail / skip 保持原样
    if issubclass(exc_type, (AssertionError, pytest.fail.Exception, pytest.skip.Exception)):
        return
    raise AssertionError(f"{exc_type.__name__}: {exc}") from exc


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用例失败时自动截图并附到 Allure 报告。"""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    instance = getattr(item, "instance", None)
    driver = getattr(instance, "driver", None) if instance else None
    if driver is None:
        return

    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="失败截图",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        # 浏览器已异常退出时截图失败，不能影响用例结果的记录
        pass


def pytest_sessionfinish(session, exitstatus):
    """--send-mail 打开时，测试结束后发送报告邮件；发送失败不影响用例退出码。"""
    if not session.config.getoption("--send-mail"):
        return

    from reports.mail_report import send_report_email

    try:
        sent, attachment = send_report_email()
        if sent:
            print(f"\n[mail] 测试报告已发送，附件: {attachment or '无（仅摘要）'}")
        else:
            print("\n[mail] 报告内容与上次发送一致，已跳过发送")
    except Exception as exc:
        print(f"\n[mail] 报告发送失败: {exc}")
