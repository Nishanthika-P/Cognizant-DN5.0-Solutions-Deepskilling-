# Hands-On 7 — Migrations & Versioning

**Digital Nurture 5.0 | Module 3 | Database Integration**

---

## Folder Structure

```
hands_on_7/
├── migrations_project/          # SQLAlchemy + Alembic (main solution)
│   ├── alembic.ini              # Alembic config — update DB credentials here
│   ├── models.py                # All 5 ORM models (incl. is_active + CourseSchedule)
│   ├── run_migrations.py        # Automated demo of all 3 tasks
│   └── migrations/
│       ├── env.py               # Alembic env — imports Base for autogenerate
│       ├── script.py.mako       # Migration file template
│       └── versions/
│           ├── 001_initial_schema.py            # Task 1 — 5 base tables
│           ├── 002_add_is_active_to_students.py # Task 2 — is_active column
│           └── 003_add_course_schedule_table.py # Task 2 — CourseSchedule table
└── django_demo/                 # Bonus — Django ORM equivalent
    ├── models.py                # Django models mirroring the schema
    └── django_migrations_demo.py # manage.py command 
```

This executes **all three tasks** in sequence:

| Step | Command | Effect |
|------|---------|--------|
| Task 1 | `alembic upgrade a1b2c3d4e5f6` | Creates 5 base tables |
| Task 2a | `alembic upgrade b2c3d4e5f6a1` | Adds `is_active` to students |
| Task 2b | `alembic upgrade c3d4e5f6a1b2` | Creates `course_schedules` |
| Task 3a | `alembic downgrade -1` | Drops `course_schedules` |
| Task 3b | `alembic downgrade base` | Drops ALL tables |
| Task 3c | `alembic upgrade head` | Re-applies everything |

---

## Manual Commands (step-by-step reference)

```bash
# Check current revision
alembic current

# Apply all migrations
alembic upgrade head

# View migration history
alembic history --verbose

# Roll back one step
alembic downgrade -1

# Roll back everything
alembic downgrade base

# Generate a new migration after editing models.py
alembic revision --autogenerate -m "describe your change"
```

---

## Migration Chain

```
None
 └─► a1b2c3d4e5f6  (001) initial schema
      └─► b2c3d4e5f6a1  (002) add is_active to students
           └─► c3d4e5f6a1b2  (003) add course_schedules table  ← HEAD
```

---

## Task Checklist

### Task 1 — Set Up Alembic (Steps 92–97)
- [x] `alembic init migrations` structure created
- [x] `alembic.ini` configured with `sqlalchemy.url`
- [x] `env.py` imports `Base` and sets `target_metadata`
- [x] `001_initial_schema.py` contains `upgrade()` and `downgrade()`
- [x] `alembic_version` table created on first `upgrade`

### Task 2 — Incremental Migrations (Steps 98–103)
- [x] `is_active BOOLEAN DEFAULT TRUE` added to `Student` model
- [x] Migration `002` generated — `upgrade()` adds column, `downgrade()` drops it
- [x] `CourseSchedule` model added with FK → courses
- [x] Migration `003` generated for the new table
- [x] `alembic history verbose` shows 3 revisions

### Task 3 — Rollback & Recovery (Steps 104–107)
- [x] `alembic downgrade -1` drops `course_schedules`
- [x] `alembic downgrade base` drops all tables
- [x] `alembic upgrade head` restores full schema
- [x] `alembic current` confirms head revision

### Bonus — Django Migrations (Step 108)
- [x] `django_demo/models.py` mirrors the schema
- [x] `django_migrations_demo.py` shows `makemigrations`, `migrate`, rollback
- [x] `select_related` example avoids N+1 (links to Hands-On 6)
