import subprocess
import sys
import os


def run(cmd: str, label: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  CMD: {cmd}")
    print("=" * 60)
    result = subprocess.run(cmd, shell=True, text=True)
    if result.returncode != 0:
        print(f"[WARNING] Command exited with code {result.returncode}")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — Baseline migration
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "█" * 60)
print("  TASK 1: Generate and apply the initial migration")
print("█" * 60)


run("python manage.py makemigrations college --name initial_schema",
    "Generate 0001_initial_schema.py from models.py")


run("python manage.py migrate college",
    "Apply migration — creates all tables + django_migrations tracking table")

run("python manage.py showmigrations college",
    "Verify: [X] 0001_initial_schema")

# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — Incremental migrations
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "█" * 60)
print("  TASK 2: Incremental migrations")
print("█" * 60)

run("python manage.py makemigrations college --name add_is_active_and_schedule",
    "Generate 0002_add_is_active_and_schedule.py")

run("python manage.py migrate college",
    "Apply: is_active column added, course_schedules table created")

run("python manage.py showmigrations college --verbosity 2",
    "View full migration chain — expect 2 migrations, both applied [X]")

# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — Rollback and Recovery
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "█" * 60)
print("  TASK 3: Rollback and Recovery")
print("█" * 60)

# Step 105: Roll back one migration (equivalent to alembic downgrade -1)
run("python manage.py migrate college 0001_initial_schema",
    "Step 105 — Roll back to 0001: is_active and course_schedules DROPPED")

run("python manage.py showmigrations college",
    "Verify: [X] 0001_initial_schema  [ ] 0002_add_is_active_and_schedule")

# Step 106: Roll back to zero (equivalent to alembic downgrade base)
run("python manage.py migrate college zero",
    "Step 106 — Roll back to zero: ALL college tables DROPPED")

run("python manage.py showmigrations college",
    "Verify: [ ] 0001  [ ] 0002  (nothing applied)")

# Step 107: Re-apply everything
run("python manage.py migrate college",
    "Step 107 — Re-apply all: back to full schema")

run("python manage.py showmigrations college",
    "Verify: [X] 0001  [X] 0002  (all applied)")

print("\n" + "█" * 60)
print("  Django migration demo COMPLETE")
print("█" * 60)



BONUS_QUERY_EXAMPLE = """
# In a Django shell (python manage.py shell):

from college.models import Enrollment

# ── N+1 version (BAD) ────────────────────────────────────────────
enrollments = Enrollment.objects.all()
for e in enrollments:
    print(e.student.first_name, '→', e.course.course_name)
# Issues 1 + N + N queries (one per student, one per course)

# ── Fixed with select_related (GOOD) ─────────────────────────────
enrollments = Enrollment.objects.select_related('student', 'course').all()
for e in enrollments:
    print(e.student.first_name, '→', e.course.course_name)
# Issues exactly 1 query with JOINs — same data, zero extra round-trips
"""

print("\nBONUS — select_related example (copy into Django shell):")
print(BONUS_QUERY_EXAMPLE)
