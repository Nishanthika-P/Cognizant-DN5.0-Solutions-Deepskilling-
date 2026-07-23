"""
Hands-On 6 - conftest.py
Shared pytest fixtures for the Selenium Playground test suite.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Step 48: session-scoped base_url fixture, reused across all tests
@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


# Step 41: function-scoped driver fixture - a fresh browser per test
# scope='function' -> new browser instance per test, tests are fully
# isolated from each other (no shared state / cookies / open dialogs).
# scope='session' would reuse a single browser across all tests, which is
# faster but risks one test's leftover state (cookies, open tabs, alerts)
# leaking into and breaking the next test.
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)

    yield drv  # --- setup above, test runs here ---

    drv.quit()  # --- teardown after yield ---


# Step 46: capture a screenshot automatically when a test fails
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            test_name = item.name.replace("/", "_")
            screenshot_path = f"{test_name}_failure.png"
            driver_fixture.save_screenshot(screenshot_path)
            print(f"\nFailure screenshot saved: {screenshot_path}")
