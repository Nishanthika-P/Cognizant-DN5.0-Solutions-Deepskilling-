# Hands-On 7 — FastAPI: Dependency Injection, CRUD & OpenAPI Documentation

## Setup
```bash
pip install -r requirements.txt
cd fastapi_coursemanager
uvicorn main:app --reload
```

## Test
```
POST   http://127.0.0.1:8000/api/courses/                -> 201
DELETE http://127.0.0.1:8000/api/courses/1                -> 204 (no body)
GET    http://127.0.0.1:8000/api/courses/999               -> 404 JSON detail
GET    http://127.0.0.1:8000/api/courses/1/students/       -> enrolled students (JOIN)
POST   http://127.0.0.1:8000/api/students/                -> 201
POST   http://127.0.0.1:8000/api/enrollments/             -> 201 immediately;
        check the server console afterwards for
        "Sending confirmation to <email>" (background task)
```

Visit `http://127.0.0.1:8000/docs` to see endpoints grouped by tag
(`Courses`, `Students`, `Enrollments`) with custom summaries.

## Files
- `models.py` — full ORM schema: `Department`, `Course`, `Student`, `Enrollment`
- `schemas.py` — Pydantic schemas for all four entities
- `main.py` — complete CRUD for Courses/Students/Enrollments, `HTTPException`
  404s, `response_model` + correct status codes (201/204), `BackgroundTasks`
  on enrollment creation, and OpenAPI title/description/version/contact +
  per-route tags/summary/response_description

## Expected Outcome
`DELETE` returns 204 with no body. `POST` returns 201 with the created
resource. Invalid IDs return 404 with a JSON `detail` message. Enrollment
creation returns immediately while the confirmation "email" prints to the
console afterward. `/docs` shows grouped, described endpoints.
