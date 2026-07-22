# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

**Module:** QA Concepts & Test Automation — Selenium Basics
**System Under Test:** Course Management API

---

## Task 1: Map Testing Types to a Real System

### 1. Test Cases by Test Level

**Unit Testing** (single function in isolation)
- **Test Case:** Test the `validate_course_code()` function directly, passing a code like `"CS"` (too short) and asserting it raises a `ValidationError` / returns `False`, without starting the API server or touching the database.

**Integration Testing** (two components working together)
- **Test Case:** Call the `POST /api/courses/` endpoint handler with a valid payload and verify that a corresponding row is correctly inserted into the `courses` table in the database — testing the interaction between the API layer and the persistence layer.

**System Testing** (full end-to-end flow)
- **Test Case:** Send an HTTP `POST /api/courses/` request over the network to the running application, with a valid JSON body, and verify: the HTTP response is `201 Created`, the response body contains the correct course data, and a subsequent `GET /api/courses/{id}` returns the same data — validating the complete request → processing → database → response cycle.

**User Acceptance Testing** (perspective of an actual college admin user)
- **Test Case:** As a college admin, log in to the admin portal, use the "Add Course" form to create a new course called "Data Structures" with code "CS201," submit it, and confirm the course appears in the course listing page exactly as entered — validating the feature meets the real business need, not just the technical contract.

### 2. Functional vs Non-Functional Classification

| Test Case | Classification |
|---|---|
| Unit test — `validate_course_code()` | Functional |
| Integration test — API + DB insert | Functional |
| System test — full POST → GET flow | Functional |
| UAT — admin creates course via UI | Functional |

**Non-Functional Example:**
**Performance Test:** Send 100 concurrent `POST /api/courses/` requests and verify the 95th percentile response time stays under 500ms and no requests fail under load. This tests *how well* the system performs, not *whether* it performs the correct action.

### 3. Black-Box vs White-Box Testing

- **Black-Box Testing:** Testing the application's behavior purely from its external inputs and outputs, with no knowledge of the internal code, algorithms, or database structure. The tester only knows "if I send X, I should get Y."
- **White-Box Testing:** Testing with full knowledge of the internal code structure, logic branches, and implementation details — used to verify internal paths, edge cases in logic, and code coverage.

**Who performs which:**
- A **QA tester** typically performs **Black-Box testing** — validating the system meets requirements from a user's/consumer's perspective.
- A **Developer** typically performs **White-Box testing** — writing unit tests that exercise specific internal logic branches, since they have direct knowledge of the code.

### 4. Formal Test Cases — `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC_COURSE_001 | Create course with valid data | API server is running; DB is accessible; no course with code "CS301" exists | 1. Send `POST /api/courses/` with body `{"name": "Operating Systems", "code": "CS301", "credits": 4}`  2. Capture response | Response status `201 Created`; response body contains the submitted course data plus a generated `id`; record exists in DB | | |
| TC_COURSE_002 | Create course with duplicate course code | A course with code "CS301" already exists in the DB | 1. Send `POST /api/courses/` with body `{"name": "OS Advanced", "code": "CS301", "credits": 3}` | Response status `400 Bad Request` or `409 Conflict`; error message indicates duplicate course code; no new record created | | |
| TC_COURSE_003 | Create course with missing required field | API server is running | 1. Send `POST /api/courses/` with body `{"name": "Operating Systems"}` (missing `code`) | Response status `422 Unprocessable Entity` / `400 Bad Request`; error message specifies `code` field is required; no record created | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle

```
        ┌────────┐
        │  New   │  ← Defect reported by QA
        └───┬────┘
            │
            ▼
       ┌──────────┐
       │ Assigned │  ← Lead assigns to a developer
       └────┬─────┘
            │
            ▼
       ┌─────────┐
       │  Open   │  ← Developer starts working on the fix
       └───┬─────┘
            │
            ▼
       ┌─────────┐
       │  Fixed  │  ← Developer completes the code fix
       └───┬─────┘
            │
            ▼
       ┌──────────┐
       │ Retest   │  ← QA re-verifies the fix in the build
       └───┬──────┘
            │
     ┌──────┴──────┐
     ▼             ▼
┌──────────┐  ┌─────────┐
│ Verified │  │ Reopened│ ← If retest fails, goes back to Open
└────┬─────┘  └─────────┘
     │
     ▼
┌─────────┐
│ Closed  │  ← Confirmed fixed, defect closed permanently
└─────────┘
```

**Additional paths:**
- **Rejected:** From `New`/`Assigned`, if the reported behavior is not actually a defect (e.g., it's "working as designed" or a duplicate), the developer/lead marks it **Rejected**, with justification, instead of moving to `Open`.
- **Deferred:** From `Assigned`/`Open`, if the defect is valid but low priority or out of scope for the current release, it is marked **Deferred** — to be revisited in a future release/sprint, rather than fixed immediately.

### 6. Severity & Priority Classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| (a) `POST /api/courses/` returns `500` for **all** requests | **Critical** | **P1** | Core functionality is completely broken for every user — no course can be created at all. This blocks the primary business function of the system. |
| (b) Course names >150 chars are silently truncated, no error | **Medium** | **P3** | Doesn't crash the system, but produces incorrect/silent data corruption. Affects data integrity but only for an edge-case input length; users aren't blocked from normal use. |
| (c) Typo in the `/docs` Swagger description | **Low** | **P4** | Purely cosmetic/documentation issue. Has zero impact on functionality; can be fixed whenever convenient. |
| (d) Login with correct credentials intermittently returns `401` | **High** | **P2** (often escalated to P1) | Impact is high (users are locked out unpredictably) even though it doesn't happen every time. Intermittent auth failures erode user trust and are hard to reproduce — marked high priority to catch it before it worsens. |

### 7. Defect Report — Bug (a)

| Field | Detail |
|---|---|
| **Defect ID** | DEF-1042 |
| **Title** | `POST /api/courses/` returns 500 Internal Server Error for all requests |
| **Environment** | Staging — Ubuntu 22.04, Python 3.11, PostgreSQL 15 |
| **Build Version** | v2.3.1-rc1 |
| **Severity** | Critical |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Ensure API is running on staging.  2. Send `POST /api/courses/` with a valid JSON body (e.g., `{"name": "Data Structures", "code": "CS201", "credits": 4}`) via Postman or curl.  3. Observe the response. |
| **Expected Result** | `201 Created` response with the newly created course object in the response body. |
| **Actual Result** | `500 Internal Server Error` is returned for every request, regardless of payload validity. |
| **Attachments** | screenshot of 500 error |

### 8. Severity vs Priority

- **Severity** measures the **impact of the defect on the system's functionality** — how badly it breaks things technically.
- **Priority** measures **how urgently the defect needs to be fixed**, based on business needs, visibility, and timelines — independent of technical impact.

**Real-world example — High Severity, Low/Medium Priority:**
A bug where the "Export to PDF" feature (used by <1% of users, once a month) crashes the entire export module has **High Severity** (the feature is completely broken), but if the release deadline is tomorrow and this feature is rarely used, the team may assign it **Low/Medium Priority** — to be fixed in a hotfix next week rather than delaying the release.

**Conversely (Low Severity, High Priority):** A misspelled company name on the CEO's personal dashboard is **Low Severity** (doesn't break any functionality) but may get **High Priority** because of visibility and reputational concerns.
