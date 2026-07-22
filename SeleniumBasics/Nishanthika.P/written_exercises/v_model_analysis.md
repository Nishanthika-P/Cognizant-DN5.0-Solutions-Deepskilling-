# Hands-On 2: SDLC vs TDLC — V-Model & Agile QA Integration

**Track:** Digital Nurture 5.0 — Python Full Stack Engineer
**System Under Test:** Course Management API

---

## Task 1: V-Model Mapping

### 9. V-Model Diagram (ASCII)

```
   DEVELOPMENT (Left)                        TESTING (Right)
   ───────────────────                       ───────────────────
   Requirements  ─────────────────────────►  Acceptance Testing
        │                                             ▲
        ▼                                             │
   System Design ─────────────────────────►  System Testing
        │                                             ▲
        ▼                                             │
   Architecture Design ────────────────────►  Integration Testing
        │                                             ▲
        ▼                                             │
   Module Design ──────────────────────────►  Unit Testing
        │                                             ▲
        ▼                                             │
                     ┌──────────────┐
                     │    Coding    │  ← Bottom vertex of the "V"
                     └──────────────┘
```

Each development phase on the left has a **direct, horizontal relationship** to a corresponding testing phase on the right — the testing plan for each level is written *while* the matching development phase is happening, not after coding is complete.

### 10. Test Artifacts Produced per Development Phase

| SDLC Phase | TDLC Phase (Right Side) | Test Artifact Produced |
|---|---|---|
| Requirements | Acceptance Testing | Acceptance Test Plan / Acceptance Criteria (e.g., Gherkin scenarios) written from user stories |
| System Design | System Testing | System Test Plan — covering end-to-end flows across all modules (e.g., API request → DB → response) |
| Architecture Design | Integration Testing | Integration Test Plan — identifying which components/interfaces (e.g., API layer ↔ DB layer) need interface-level tests |
| Module Design | Unit Testing | Unit Test Plan / Test Case list — one per function or class method defined in the module design |

### 11. Entry & Exit Criteria per TDLC Phase

| Testing Level | Entry Criteria | Exit Criteria |
|---|---|---|
| **Unit Testing** | Module design finalized; code for the unit is compiled/committed; unit test cases are written | All unit test cases executed; code coverage meets the agreed threshold (e.g., 80%); no open critical defects at unit level |
| **Integration Testing** | All relevant unit tests pass; interfaces between components (e.g., API + DB) are defined and available | All integration test cases executed; all interface defects resolved; data flows correctly between integrated components |
| **System Testing** | Integration testing complete and signed off; full application build deployed to a test environment; test data available | All planned system test cases executed; defect count below the agreed threshold; no open critical/high defects; all functional and non-functional requirements verified |
| **Acceptance Testing (UAT)** | System testing complete and signed off; UAT environment configured with production-like data; business stakeholders/admin users available | Business stakeholders formally approve the system meets acceptance criteria; no open critical/high defects; sign-off documented for release |

### 12. Two Early QA Engagement Points (Course Management API)

1. **Requirements Review stage:** QA reviews the user stories/requirements for the Course Management API (e.g., "create a course," "prevent duplicate course codes") *before* any code is written, to catch ambiguous or untestable requirements early — for example, flagging that "course code must be unique" needs a precise definition of what happens on a duplicate (error code, message).
2. **Architecture/API Contract Design stage:** QA reviews the proposed API contract (endpoint names, request/response schemas, status codes) during the Architecture Design phase, to identify missing error-handling paths or inconsistent status codes before Integration Testing begins — preventing costly rework later.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three Problems with Waterfall (Testing After Development)

1. **Defects found late are expensive to fix.** If a design flaw in the Course Management API (e.g., the database schema doesn't support unique course codes) is only discovered during system testing, fixing it may require reworking the schema, migrations, and all dependent code — far more costly than catching it at the requirements stage.
2. **Compressed testing timelines under deadline pressure.** Since testing only starts after all development finishes, any delay in coding directly eats into the testing schedule, often forcing QA to cut corners or skip test cases to hit the release date.
3. **Feedback loop is too slow.** Developers who wrote the `POST /api/courses/` endpoint weeks ago have moved on to other features by the time defects are reported, making context-switching and root-cause analysis slower and more error-prone.

### 14. QA's Role in Agile Ceremonies

| Ceremony | QA's Role |
|---|---|
| **Sprint Planning** | Defines and reviews **acceptance criteria** for each user story (e.g., for "create a course" story) to ensure it is testable and unambiguous before the team commits to it. |
| **Daily Standup** | Reports **blocking issues** — e.g., "the staging environment is down, I can't execute the course-creation test cases today" — so the team can unblock QA quickly. |
| **Sprint Review** | Performs **demo testing** — validates the completed feature live in front of stakeholders during the sprint demo, confirming it behaves as expected. |
| **Retrospective** | Contributes to **process improvement** — e.g., suggesting that flaky Selenium tests be stabilized, or that acceptance criteria need to be written earlier in future sprints. |

### 15. Four Shift-Left Practices Applied to the Course Management API

| Practice | Application to Course Management API |
|---|---|
| (a) Reviewing requirements for testability | QA reviews the user story "prevent duplicate course codes" and asks: "What HTTP status code and error message should be returned?" — clarifying it before development starts. |
| (b) Writing test cases before code (TDD/BDD) | Before implementing `POST /api/courses/`, the team writes a Gherkin scenario: "Given a course code already exists, When a duplicate is submitted, Then a 400 error is returned" — driving the implementation. |
| (c) Static code analysis | Tools like `pylint` or `flake8` run automatically in CI on every commit to the API codebase, catching code-quality issues (unused imports, complexity) before a human reviewer or tester ever sees the code. |
| (d) API contract testing before integration | Before the frontend team builds the course-creation form, the API's OpenAPI/Swagger schema is validated against agreed contracts, so integration issues (wrong field names, types) are caught before both sides are fully built. |

### 16. Acceptance Criteria in Gherkin — "Create a New Course"

```gherkin
Feature: Course Creation
  As a college admin
  I want to create a new course
  So that students can enroll in it

  Scenario: Happy path - successfully create a new course
    Given I am logged in as a college admin
    And no course with code "CS201" exists
    When I submit a new course with name "Data Structures" and code "CS201"
    Then the course should be created successfully
    And the response status should be 201 Created
    And the new course should appear in the course listing

  Scenario: Duplicate course code
    Given I am logged in as a college admin
    And a course with code "CS201" already exists
    When I submit a new course with the code "CS201"
    Then the course should not be created
    And the response status should be 400 Bad Request
    And I should see an error message indicating the course code already exists

  Scenario: Missing required fields
    Given I am logged in as a college admin
    When I submit a new course without providing a course code
    Then the course should not be created
    And the response status should be 422 Unprocessable Entity
    And I should see an error message indicating the course code field is required
```
