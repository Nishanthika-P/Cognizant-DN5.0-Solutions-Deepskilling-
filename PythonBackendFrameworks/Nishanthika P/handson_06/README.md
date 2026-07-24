# Hands-On 6 — FastAPI: Path Parameters, Pydantic & Async Endpoints

## Setup
```bash
pip install -r requirements.txt
cd fastapi_coursemanager
uvicorn main:app --reload
```

## Test
```
GET  http://127.0.0.1:8000/                                -> {"message": "API running"}
GET  http://127.0.0.1:8000/docs                             -> Swagger UI
POST http://127.0.0.1:8000/api/courses/                     -> 201 (422 on invalid body)
GET  http://127.0.0.1:8000/api/courses/1                    -> 200 or 404
GET  http://127.0.0.1:8000/api/courses/?skip=0&limit=2      -> first 2 courses
GET  http://127.0.0.1:8000/api/courses/?department_id=1     -> filtered by department
PUT  http://127.0.0.1:8000/api/courses/1                    -> 200 or 404
DELETE http://127.0.0.1:8000/api/courses/1                  -> 204 or 404
```

## Files
- `schemas.py` — `CourseCreate`, `CourseUpdate`, `CourseResponse`, and the
  nested `DepartmentResponse` (Task 1, steps 58-59)
- `database.py` — async engine (`create_async_engine`) + `get_db()`
  dependency (Task 2, step 64)
- `models.py` — SQLAlchemy ORM models (`Department`, `Course`)
- `main.py` — root route, POST with Pydantic validation, path/query
  parameters, pagination/filtering, and full async CRUD via
  Dependency Injection (Task 1 + Task 2)

## Expected Outcome
`/docs` shows the `POST /api/courses/` endpoint with the `CourseCreate`
schema; invalid data returns 422 with field-level errors. `GET
/api/courses/?limit=2` returns 2 courses; `department_id` filters
correctly. All DB operations are async (`await db.execute(...)`,
`await db.commit()`).
