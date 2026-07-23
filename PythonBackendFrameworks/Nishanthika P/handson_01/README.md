# Hands-On 1 — Web Framework Foundations & Django Project Setup

## Setup
```bash
pip install -r requirements.txt
cd coursemanager
python manage.py runserver
```


## Files
- `notes.py` — Task 1 write-up (request-response cycle, middleware, WSGI vs ASGI, MVC->MVT)
- `coursemanager/` — the Django project (Task 2)
  - `coursemanager/settings.py`, `urls.py`, `wsgi.py`, `asgi.py`
  - `courses/views.py` — `hello_view`
  - `courses/urls.py` — routes `/api/hello/`

## Expected Outcome
Browser shows "Course Management API is running" at `/api/hello/`.
`courses` app is registered in `INSTALLED_APPS`.
