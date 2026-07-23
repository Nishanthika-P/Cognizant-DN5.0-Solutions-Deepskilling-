"""
Hands-On 6 - Task 1 & Task 2
pytest test suite for the Selenium Playground, using the `driver` and
`base_url` fixtures defined in conftest.py.

Run with:
    pytest test_playground.py -v --html=report.html --self-contained-html
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pytest


# --- Step 42 / Step 45: simple form submission (parameterised) ---
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url + "simple-form-demo/")

    message_input = driver.find_element(By.ID, "user-message")
    message_input.send_keys(message)
    driver.find_element(By.CSS_SELECTOR, "#single-input button").click()

    displayed_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed_message.text == message


# --- Step 43: checkbox demo ---
def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo/")

    first_checkbox = driver.find_element(By.ID, "isAgeSelected")
    first_checkbox.click()
    assert first_checkbox.is_selected() is True

    first_checkbox.click()
    assert first_checkbox.is_selected() is False


# --- Step 49: dropdown selection ---
def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo/")

    dropdown_element = driver.find_element(By.ID, "select-demo")
    select = Select(dropdown_element)
    select.select_by_visible_text("Wednesday")

    assert select.first_selected_option.text == "Wednesday"


# --- Demonstrates the failure-screenshot hook from conftest.py ---
def test_intentional_failure_for_screenshot_demo(driver, base_url):
    """
    This test is included only to demonstrate that the
    pytest_runtest_makereport hook in conftest.py correctly captures a
    screenshot on failure. Remove or skip in a real regression suite.
    """
    driver.get(base_url)
    assert driver.title == "This Title Does Not Exist"
