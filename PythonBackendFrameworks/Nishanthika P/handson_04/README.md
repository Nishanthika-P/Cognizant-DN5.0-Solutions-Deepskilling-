# Hands-On 4 — Flask App Structure, Routing, Jinja2 & Blueprints

## Setup
```bash
pip install -r requirements.txt
cd flask_coursemanager
python app.py
```

## Test
```
GET    http://127.0.0.1:5000/api/courses/          -> []
POST   http://127.0.0.1:5000/api/courses/          -> 201 (missing fields -> 400)
GET    http://127.0.0.1:5000/api/courses/1/         -> 200 or 404
PUT    http://127.0.0.1:5000/api/courses/1/         -> 200 or 404
DELETE http://127.0.0.1:5000/api/courses/1/         -> 204 or 404
```

## Files
- `app.py` — application factory (`create_app`) + JSON 404/500 error handlers
- `config.py` — `Config` class (SECRET_KEY, SQLALCHEMY_DATABASE_URI, DEBUG)
- `courses/routes.py` — Blueprint with full CRUD, field validation,
  and the `make_response_json()` envelope helper

## Expected Outcome
All endpoints return JSON (never HTML). Missing `name`/`code`/`credits`
returns 400 with a descriptive message. Unknown IDs return 404.
