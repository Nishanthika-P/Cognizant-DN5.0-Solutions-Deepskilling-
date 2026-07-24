# Hands-On 5 — Flask with SQLAlchemy ORM & Database Integration

## Setup
```bash
pip install -r requirements.txt
cd flask_coursemanager

# macOS/Linux
export FLASK_APP=app.py
# Windows
set FLASK_APP=app.py

flask db init
flask db migrate -m "initial schema"
flask db upgrade
```

## Seed sample data (Task 1, step 51)
```bash
flask shell < ../seed_data.py
```

## Run
```bash
python app.py
```

## Files
- `flask_coursemanager/app.py` — `db = SQLAlchemy()`, `migrate = Migrate()`, wired into `create_app()`
- `flask_coursemanager/courses/models.py` — `Department`, `Course`, `Student`,
  `Enrollment` SQLAlchemy models with relationships + `to_dict()` on each
- `flask_coursemanager/courses/routes.py` — CRUD routes now read/write the
  real database (`get_or_404`), plus `/api/courses/<id>/students/` JOIN route
- `seed_data.py` — Task 1 sample-data script

## Expected Outcome
`flask db upgrade` creates all tables. All CRUD endpoints read from and
write to the database. `/api/courses/<id>/students/` returns the correct
enrolled students via a JOIN through `Enrollment`.
