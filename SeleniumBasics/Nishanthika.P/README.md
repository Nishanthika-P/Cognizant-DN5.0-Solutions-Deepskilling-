# Selenium Basics — QA Concepts & Test Automation
### Digital Nurture 5.0 | Python Full Stack Engineer Track
**Submitted by:** Nishanthika P

This repository contains solutions for all 7 Hands-On exercises covering QA fundamentals, test automation theory, and practical Selenium WebDriver automation with the Page Object Model.

---

## Folder Structure

```
SeleniumBasics/YourName/
│
├── written_exercises/
│   ├── qa_concepts.md              → Hands-On 1
│   ├── v_model_analysis.md         → Hands-On 2
│   └── automation_strategy.md      → Hands-On 3
│
├── automation_scripts/
│   ├── hands_on_4/
│   │   ├── driver_setup.py         → Task 1: architecture & environment setup
│   │   └── navigation_commands.py  → Task 2: navigation, tabs, screenshots
│   │
│   ├── hands_on_5/
│   │   ├── locator_strategies.py   → Task 1: ID/Name/CSS/XPath locators
│   │   └── wait_strategies.py      → Task 2: WebDriverWait, FluentWait
│   │
│   ├── hands_on_6_task1/
│   │   ├── conftest.py             → driver fixture only
│   │   └── test_playground.py      → plain pytest tests (Steps 40–44)
│   │
│   ├── hands_on_6_task2/
│   │   ├── conftest.py             → + base_url fixture + failure screenshot hook
│   │   └── test_playground.py      → parametrized tests (Steps 45–49)
│   │
│   └── hands_on_7/
│       ├── pages/                  → Page Object Model classes
│       │   ├── base_page.py
│       │   ├── simple_form_page.py
│       │   ├── checkbox_page.py
│       │   ├── dropdown_page.py
│       │   └── input_form_page.py
│       ├── tests/
│       │   ├── conftest.py
│       │   └── test_pom_suite.py   → full POM-based suite (Steps 55–59)
│       └── pytest.ini
│
└── requirements.txt
```

---

## Hands-On Summary

| # | Title | Type | Level | Deliverable |
|---|---|---|---|---|
| 1 | QA Concepts, Functional Testing & Defect Lifecycle | Written | Beginner | `qa_concepts.md` |
| 2 | SDLC vs TDLC — V-Model & Agile QA Integration | Written | Beginner | `v_model_analysis.md` |
| 3 | Test Automation Process, Lifecycle & Framework Types | Written | Intermediate | `automation_strategy.md` |
| 4 | Selenium WebDriver Setup, Browser Drivers & Basic Commands | Code | Intermediate | `hands_on_4/` |
| 5 | Locators — ID, Name, XPath, CSS & Explicit Waits | Code | Intermediate | `hands_on_5/` |
| 6 | Running Selenium Tests with pytest — Fixtures & Reporting | Code | Advanced | `hands_on_6_task1/`, `hands_on_6_task2/` |
| 7 | Page Object Model (POM) | Code | Advanced | `hands_on_7/` |

---

## Software & Tools Required

- Python 3.10+
- Google Chrome (latest)
- VS Code (recommended)
- pip packages: `selenium`, `pytest`, `pytest-html`, `webdriver-manager`

All required packages are listed in `requirements.txt`.

---

## Setup Instructions

```bash
# 1. Navigate to the project root
cd SeleniumBasics/YourName

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to Run Each Hands-On

### Hands-On 1–3 (Written)
No execution needed — open the `.md` files in `written_exercises/` directly.

### Hands-On 4 — Plain scripts
```bash
cd automation_scripts/hands_on_4
python driver_setup.py
python navigation_commands.py
```
✅ Confirms: page title printed, second tab opened, `playground_screenshot.png` saved.

### Hands-On 5 — Plain scripts
```bash
cd ../hands_on_5
python locator_strategies.py
python wait_strategies.py
```
✅ Confirms: all 6 locator strategies find the target element; explicit/fluent waits work without hard-coded sleeps.

### Hands-On 6 — pytest (Task 1 then Task 2)
```bash
cd ../hands_on_6_task1
pytest -v

cd ../hands_on_6_task2
pytest -v --html=report.html --self-contained-html
```
✅ Confirms: parametrized tests run as separate cases; `report.html` generated; a failure screenshot is auto-captured via the `conftest.py` hook.

### Hands-On 7 — Full POM Suite
```bash
cd ../hands_on_7
pytest tests/ -v --html=report.html --self-contained-html

# Verify zero find_element calls in test files (POM compliance check):
grep -r "find_element" tests/
```
✅ Confirms: all 4 tests pass through Page Object methods only; `grep` returns nothing, proving test files contain assertions only, no direct WebDriver calls.

---

## Key Concepts Demonstrated

- **QA Fundamentals:** test levels, functional vs non-functional testing, defect lifecycle, severity vs priority
- **V-Model & Agile:** SDLC-TDLC mapping, entry/exit criteria, Shift-Left testing, Gherkin acceptance criteria
- **Automation Strategy:** automation ROI, flaky test mitigation, framework type comparison (Linear/Modular/Data-Driven/Keyword-Driven/Hybrid)
- **Selenium WebDriver:** driver setup, headless mode, window/tab handling, screenshots
- **Locators:** ID, Name, Class, Tag, XPath (absolute & relative), CSS Selectors
- **Waits:** implicit vs explicit vs fluent waits, `ExpectedConditions`
- **pytest Integration:** fixtures, `conftest.py`, parametrization, HTML reporting, failure hooks
- **Page Object Model:** separation of test logic (assertions) from UI logic (interactions), locator centralization, maintainability

---

## Notes

- All Selenium scripts target the **LambdaTest Selenium Playground** (`https://www.lambdatest.com/selenium-playground/`), now redirecting to `testmuai.com` following a site rebrand — assertions were written to tolerate this redirect.
- Chrome runs in **headless mode** by default in all scripts; remove `--headless=new` in the driver setup if you want to visually watch the browser during debugging.
- `webdriver-manager` auto-downloads the correct ChromeDriver version — no manual driver management needed.
