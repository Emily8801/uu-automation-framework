"""浏览器创建：统一 Chrome 启动参数，支持无头模式。"""

from selenium import webdriver


def create_driver(headless: bool = False) -> webdriver.Chrome:
    """创建 Chrome driver；Selenium Manager 自动匹配 ChromeDriver。"""
    options = webdriver.ChromeOptions()
    for arg in ("--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"):
        options.add_argument(arg)

    if headless:
        # 无头模式没有真实显示器，需显式指定窗口大小
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    if not headless:
        driver.maximize_window()

    # 显式等待由页面对象统一控制，关掉隐式等待避免两者叠加
    driver.implicitly_wait(0)
    return driver
