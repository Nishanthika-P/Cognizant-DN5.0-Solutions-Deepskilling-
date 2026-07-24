# Hands-On 8 — RESTful API Design Best Practices

> Framework-agnostic hands-on; this refactors the FastAPI implementation
> from Hands-On 7 to meet all the REST design criteria. (The same
> principles apply verbatim if you pick Django or Flask instead.)

## Setup
```bash
pip install -r requirements.txt
cd fastapi_coursemanager
uvicorn main:app --reload
```

## Test
```
POST   http://127.0.0.1:8000/api/v1/courses/                        -> 201 + Location header
GET    http://127.0.0.1:8000/api/v1/courses/?page=1&page_size=2      -> {count, next, previous, results}
GET    http://127.0.0.1:8000/api/v1/courses/?search=data              -> case-insensitive name/code match
PATCH  http://127.0.0.1:8000/api/v1/courses/1/                        -> partial update (only sent fields change)
PUT    http://127.0.0.1:8000/api/v1/courses/1/                        -> full replace
GET    http://127.0.0.1:8000/api/v1/courses/999/                      -> 404 in standardised error format
```

## Files
- `errors.py` — standardised `{"error": {"code","message","field"}}` envelope
  via a global `HTTPException` handler, plus a `not_found()` helper
- `pagination.py` — `Page` schema + `build_page()` implementing the DRF-style
  `count`/`next`/`previous`/`results` envelope
- `main.py` — versioned `/api/v1/` routes, `PATCH` alongside `PUT`,
  `Location` header on every `POST`, `search=` filtering, and a code
  comment contrasting URL vs header-based versioning strategies

## Expected Outcome
All endpoints use plural nouns under `/api/v1/`. `PATCH` is implemented
alongside `PUT`. `POST` returns 201 with a `Location` header.
`GET /api/v1/courses/?page=1&page_size=2` returns the correct pagination
envelope. Error responses follow the standardised `{"error": {...}}` format.
