"""
Hands-On 4 - Task 1: Selenium Architecture and Environment Setup

SELENIUM COMPONENTS OVERVIEW
-----------------------------
1. WebDriver:
   The core API/library that lets code (Python, Java, etc.) send commands
   directly to a real browser. It communicates with the browser via the
   browser's native automation interface (e.g., Chrome's DevTools Protocol,
   through the ChromeDriver executable) using the W3C WebDriver protocol
   (JSON over HTTP under the hood). There is no browser plugin required -
   the driver executable acts as a bridge/server between your script and
   the actual browser process.

2. Selenium Grid:
   Solves the problem of running tests in PARALLEL across multiple
   machines and/or multiple browser/OS combinations at the same time.
   Instead of running 50 tests sequentially on one machine (slow), Grid
   distributes them across a pool of "node" machines, each running a
   different browser/OS, dramatically cutting total execution time and
   enabling cross-browser coverage.

3. Selenium IDE:
   A browser extension used for RECORD AND PLAYBACK of test steps. A user
   clicks through the application in the browser, and Selenium IDE records
   those actions as a reusable test script. It can also export the
   recorded steps as code (e.g., Python + pytest, Java + JUnit), which is
   useful for quickly bootstrapping a test or for non-programmers to get
   started, though it is best used for the "Linear" framework style
   discussed in Hands-On 3, not for a maintainable suite.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def build_driver(headless: bool = False):
    """Create and return a configured Chrome WebDriver instance."""
    options = Options()

    # Step 27: run headless - no visible browser window, still fully functional
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    # webdriver-manager auto-downloads the ChromeDriver version that
    # matches the installed Chrome browser, so no manual driver management.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Step 26: implicit wait
    # An implicit wait tells the driver to poll the DOM for up to N seconds
    # whenever ANY find_element call doesn't immediately find a match.
    # It's considered bad practice as a global default because:
    #   1. It applies to EVERY locator call in the whole session, even ones
    #      that don't need it, silently slowing down failure detection
    #      (a genuinely missing element still waits the full timeout).
    #   2. It cannot express conditions like "wait until clickable" or
    #      "wait until text changes" - only "wait until present in DOM".
    #   3. Mixing implicit waits with explicit waits (WebDriverWait) can
    #      cause unpredictable, inconsistent timing behavior.
    # Explicit waits (Hands-On 5) are preferred because they target a
    # specific condition on a specific element, only where needed.
    driver.implicitly_wait(10)

    return driver


def test_open_playground_and_print_title():
    """Step 25 & 27: open the playground, print title, close browser."""
    driver = build_driver(headless=True)
    try:
        driver.get("https://www.lambdatest.com/selenium-playground/")
        print("Page title:", driver.title)
        assert "Selenium" in driver.title or "Playground" in driver.title
    finally:
        driver.quit()


if __name__ == "__main__":
    test_open_playground_and_print_title()
