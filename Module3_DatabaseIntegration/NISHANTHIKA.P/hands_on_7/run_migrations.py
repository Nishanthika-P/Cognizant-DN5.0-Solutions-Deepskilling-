
import subprocess
import sys


def run(cmd: str, label: str) -> None:
    """Run an alembic shell command and print a clear separator."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  CMD: {cmd}")
    print("=" * 60)
    result = subprocess.run(cmd, shell=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Command failed with exit code {result.returncode}")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — Set up Alembic and apply the initial schema (Steps 92–97)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "█" * 60)
print("  TASK 1: Baseline Migration — Initial Schema")
print("█" * 60)

run("alembic upgrade a1b2c3d4e5f6",
    "Apply Migration 1: Create departments, students, courses, enrollments, professors")

run("alembic current",
    "Verify: alembic_version table now holds revision a1b2c3d4e5f6")

# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — Incremental migrations (Steps 98–103)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "█" * 60)
print("  TASK 2: Incremental Migrations")
print("█" * 60)

run("alembic upgrade b2c3d4e5f6a1",
    "Apply Migration 2: Add is_active (BOOLEAN DEFAULT TRUE) to students")

run("alembic upgrade c3d4e5f6a1b2",
    "Apply Migration 3: Create course_schedules table")

run("alembic history --verbose",
    "Show full migration chain — expect 3 revisions")

run("alembic current",
    "Confirm we are at head: c3d4e5f6a1b2")

# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — Rollback and Recovery (Steps 104–107)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "█" * 60)
print("  TASK 3: Rollback and Recovery")
print("█" * 60)

run("alembic current",
    "Step 104 — Note current head before rollback")

run("alembic downgrade -1",
    "Step 105 — Roll back one step: course_schedules table DROPPED")

run("alembic current",
    "Confirm we are now at b2c3d4e5f6a1 (is_active still exists)")

run("alembic downgrade base",
    "Step 106 — Roll back to base: ALL tables DROPPED")

run("alembic current",
    "Confirm no migration is active (empty output expected)")

run("alembic upgrade head",
    "Step 107 — Re-apply ALL migrations; back to full schema")

run("alembic current",
    "Confirm head = c3d4e5f6a1b2 (latest revision)")

print("\n" + "█" * 60)
print("  ALL TASKS COMPLETE")
print("  Schema is at latest revision with all tables and columns.")
print("█" * 60)
