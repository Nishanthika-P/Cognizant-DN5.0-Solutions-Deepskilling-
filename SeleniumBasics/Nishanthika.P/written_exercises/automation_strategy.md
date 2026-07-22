# Hands-On 3: Test Automation Process, Lifecycle & Framework Types

**System Under Test:** Course Management API / Frontend

---

## Task 1: Automation Decision and Test Case Selection

### 17. Five Criteria for Deciding What to Automate

Applied to: *"Test that `POST /api/courses/` returns 201 with the correct course data when valid input is provided."*

| Criterion | Explanation | Applied to this test case |
|---|---|---|
| **1. Repeatability** | Is the test run often (regression, every build)? | Yes — this is a core happy-path test that will be run on every commit/build. Strong candidate. |
| **2. Stability of the feature** | Does the feature under test change frequently? | The `POST /api/courses/` contract is stable and unlikely to change often once defined — good for automation, since automated tests need a stable target. |
| **3. High business risk** | Would a failure here cause significant business impact? | Yes — course creation is a core function of the system; failures here block all downstream activity (enrollment, etc.). |
| **4. Data-driven nature** | Can the test be run with multiple input combinations easily? | Yes — the test can easily be parameterised with multiple valid course payloads. |
| **5. Time savings vs manual effort** | Does automating save significant time over repeated manual execution? | Yes — this test would otherwise need to be manually re-verified on every release; automation pays off quickly given how often it will run. |

**Conclusion:** This test case meets all 5 criteria strongly — it should be automated.

### 18. Automate vs Manual Decisions

| Test Case | Decision | Justification |
|---|---|---|
| (a) Regression test for all CRUD endpoints after every code change | **Automate** | Repetitive, runs on every change, high value from automation — the textbook case for automation. |
| (b) Exploratory testing of a new search feature | **Manual** | Exploratory testing relies on human intuition and creativity to find unexpected issues; it's inherently unscripted and not suited to automation. |
| (c) Performance test: 100 concurrent users on `GET /api/courses/` | **Automate** (using a performance tool, e.g., Locust/JMeter, not Selenium) | Manually simulating 100 concurrent users is impossible; automation is the only practical approach, though it uses performance-testing tools rather than functional automation. |
| (d) UI test for the login form | **Automate** | Straightforward, repeatable functional flow, ideal for Selenium regression coverage. |
| (e) Verify the API documentation (Swagger) is accurate | **Manual** | Requires human judgment to compare documented behavior against actual behavior/intent; low ROI to automate a one-off documentation review. |
| (f) Smoke test: verify the API is reachable after deployment | **Automate** | Runs after every deployment, is simple and fast, and provides quick fail-fast feedback — ideal automation candidate as part of a CI/CD pipeline. |

### 19. Automation ROI Calculation

**Given:**
- Manual execution time: 30 minutes/run
- Automation build time (one-time): 4 hours = 240 minutes
- After the 10th run, a 20% maintenance overhead is added per run

**Definition:** Test automation ROI measures whether the time invested in building and maintaining an automated test is recovered through the cumulative time saved versus running the test manually, over its lifetime of use.

**Calculation:**

*Runs 1–10 (no maintenance overhead):*
- Time saved per run = 30 minutes (manual cost avoided)
- Break-even point (ignoring overhead): 240 minutes ÷ 30 minutes/run = **8 runs**

So, without any overhead, automation pays for itself at **run 8** — well within the first 10 runs, before the maintenance overhead even kicks in.

*Verification:*
- Cumulative manual cost after 8 runs = 8 × 30 = 240 minutes
- Cumulative automation cost after 8 runs = 240 minutes (build) + negligible run cost (assume near-instant/parallel execution) ≈ 240 minutes
- **Break-even ≈ 8 runs.**

*Beyond run 10 (with 20% maintenance overhead per run):*
- Even factoring in extra maintenance cost after run 10, the automation has already paid for itself by run 8 — the overhead only affects the *margin* of savings on subsequent runs, not whether it breaks even.

**Conclusion: Automation pays for itself after approximately 8 runs**, and remains net-positive afterward since maintenance overhead is much smaller than the 30-minute manual cost it continues to save each run.

### 20. Flaky Tests

**Definition:** A flaky test is a test that produces inconsistent results (sometimes pass, sometimes fail) without any change to the code under test — the failure is caused by the test itself (timing, environment, test data) rather than a genuine defect.

**Example:** A Selenium test that clicks "Submit" and immediately checks for a success message, without waiting for the AJAX call to complete — it passes when the network is fast and fails when it's slow, even though the application behaves correctly both times.

**3 Strategies to Prevent/Fix Flaky Tests:**
1. **Replace hard-coded `sleep()` calls with explicit waits** (`WebDriverWait` + `ExpectedConditions`) so the test waits precisely for the required state rather than a guessed fixed duration.
2. **Ensure test isolation** — each test should set up its own data and clean up afterward, so tests don't depend on execution order or leftover state from a previous run.
3. **Run tests in a stable, consistent environment** — pin browser/driver versions, avoid shared test environments where other processes can interfere, and control test data (e.g., reset the database before each run) to eliminate environmental variability.

---

## Task 2: Compare Automation Framework Types

### 21. Comparison of the 5 Framework Types

**Linear (Record & Playback) Framework**
- **Description:** Test steps are recorded directly against the application (e.g., via Selenium IDE) and played back exactly as recorded, with no reusable functions or abstraction — each script is self-contained and independent.
- **Advantage:** Very fast to create — no programming skill required, good for quick, one-off scripts.
- **Disadvantage:** Extremely hard to maintain — any UI change requires re-recording or manually editing every script that touches that element; massive code duplication.
- **Use case:** A one-time smoke check of the Course Management login page before a demo, where long-term maintenance isn't a concern.

**Modular Framework**
- **Description:** The application is broken into logical modules (e.g., login, course creation, course search), each with its own small reusable test script/function, which are then combined to build larger test scenarios.
- **Advantage:** Changes to one module (e.g., login steps) only need to be updated in one place and are reflected everywhere that module is reused.
- **Disadvantage:** Still requires programming knowledge to build and combine modules; test data is typically still hardcoded within scripts.
- **Use case:** Reusing a "login" module across many test scripts for the Course Management frontend (e.g., admin login, then create course; admin login, then delete course).

**Data-Driven Framework**
- **Description:** Test logic is separated from test data — the same script is executed multiple times with different sets of input data pulled from an external source (CSV, Excel, JSON).
- **Advantage:** Massively increases test coverage without duplicating test scripts — one script can validate dozens of input combinations.
- **Disadvantage:** Requires careful design of the data source and mapping logic; debugging failures across many data sets can be harder to trace.
- **Use case:** Testing the course-creation form with 50 different combinations of valid/invalid course names, codes, and credit values.

**Keyword-Driven Framework**
- **Description:** Test steps are represented as "keywords" (e.g., `Login`, `EnterCourseName`, `ClickSubmit`) stored in a table/spreadsheet, with an underlying engine that maps each keyword to the actual automation code.
- **Advantage:** Non-technical team members (e.g., manual QA, business analysts) can write and understand tests without knowing Selenium/Python.
- **Disadvantage:** Significant upfront investment to build the keyword engine/library; can obscure logic and be harder to debug for complex scenarios.
- **Use case:** Allowing a non-technical business analyst to define a new test scenario for the Course Management admin portal by combining existing keywords, without writing code.

**Hybrid Framework**
- **Description:** Combines elements of Modular (reusable functions), Data-Driven (external test data), and optionally Keyword-Driven (abstraction for non-technical users) into a single framework tailored to the project's needs — this is what most real-world Selenium/pytest suites use (often paired with Page Object Model).
- **Advantage:** Gets the best of all worlds — reusability, data coverage, and (optionally) accessibility for non-technical testers.
- **Disadvantage:** More complex to design and set up initially; requires a clear architecture and team discipline to avoid it becoming disorganized.
- **Use case:** The full Course Management Selenium suite — Page Objects (Modular) + parametrized pytest fixtures reading from CSV/JSON (Data-Driven) for login and course-creation tests.

### 22. Recommended Framework for the Given Scenario

**Scenario:** Test login with 50 different user/password combinations, reuse login steps across 20 test cases, support both technical and non-technical team members.

**Recommendation: Hybrid Framework** (Modular + Data-Driven, with optional lightweight Keyword-Driven layer)

**Justification:**
- The need to **reuse login steps across 20 test cases** points directly to a **Modular** design (a single `login()` function used everywhere).
- The need for **50 different user/password combinations** points to a **Data-Driven** approach (parametrize the login test with an external data file/pytest `@parametrize`).
- The need for **non-technical team members** to write tests suggests adding a thin **Keyword-Driven** layer on top (e.g., a simple table of "action" keywords that map to the underlying Modular functions), so testers without Python experience can still contribute new scenarios.
- No single "pure" framework covers all three requirements — only a **Hybrid** approach combining Modular + Data-Driven + optional Keyword abstraction satisfies all three constraints simultaneously.

### 23. Hybrid Framework Folder Structure

```
course_management_tests/
│
├── config/
│   └── config.yaml              # base_url, browser type, timeouts, environment settings
│
├── test_data/
│   ├── login_credentials.csv    # 50 user/password combinations
│   └── course_data.json         # sample course payloads for data-driven tests
│
├── pages/                       # Page Object files (Modular reusability)
│   ├── base_page.py
│   ├── login_page.py
│   ├── course_creation_page.py
│   └── dropdown_page.py
│
├── utils/
│   ├── driver_factory.py        # WebDriver initialization/teardown helpers
│   ├── data_reader.py           # helpers to read CSV/JSON test data
│   └── wait_helpers.py          # custom explicit wait wrappers
│
├── tests/                       # Test files (assertions live here only)
│   ├── test_login.py            # parametrized with login_credentials.csv
│   ├── test_course_creation.py
│   └── conftest.py              # shared pytest fixtures (driver, base_url)
│
├── reports/
│   └── report.html              # pytest-html output
│
├── requirements.txt
└── pytest.ini
```
