from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# ── Revision identifiers ──────────────────────────────────────────────────────
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = None     
branch_labels: Union[str, Sequence[str], None] = None
depends_on:    Union[str, Sequence[str], None] = None
# ─────────────────────────────────────────────────────────────────────────────


def upgrade() -> None:
    """
    Create all five tables.
    Order matters: referenced tables (departments) must be created before
    tables that hold foreign keys pointing to them.
    """

    # 1. departments — no foreign keys, create first
    op.create_table(
        "departments",
        sa.Column("department_id", sa.Integer(),    primary_key=True, autoincrement=True),
        sa.Column("dept_name",     sa.String(100),  nullable=False),
        sa.Column("head_of_dept",  sa.String(100)),   # renamed from hod_name
        sa.Column("budget",        sa.Numeric(12, 2)),
    )

    # 2. students — FK → departments
    op.create_table(
        "students",
        sa.Column("student_id",      sa.Integer(),    primary_key=True, autoincrement=True),
        sa.Column("first_name",      sa.String(50),   nullable=False),
        sa.Column("last_name",       sa.String(50),   nullable=False),
        sa.Column("email",           sa.String(100),  nullable=False, unique=True),
        sa.Column("date_of_birth",   sa.Date()),
        sa.Column("department_id",   sa.Integer(),    sa.ForeignKey("departments.department_id")),
        sa.Column("enrollment_year", sa.Integer()),
    )

    # 3. courses — FK → departments
    op.create_table(
        "courses",
        sa.Column("course_id",    sa.Integer(),    primary_key=True, autoincrement=True),
        sa.Column("course_name",  sa.String(150),  nullable=False),
        sa.Column("course_code",  sa.String(20),   unique=True),
        sa.Column("credits",      sa.Integer()),
        sa.Column("max_seats",    sa.Integer(),    server_default="60"),
        sa.Column("department_id",sa.Integer(),    sa.ForeignKey("departments.department_id")),
    )

    # 4. enrollments — FK → students, FK → courses
    op.create_table(
        "enrollments",
        sa.Column("enrollment_id",   sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("student_id",      sa.Integer(), sa.ForeignKey("students.student_id")),
        sa.Column("course_id",       sa.Integer(), sa.ForeignKey("courses.course_id")),
        sa.Column("enrollment_date", sa.Date()),
        sa.Column("grade",           sa.String(2)),
        # Composite unique index — prevents duplicate enrollments (Hands-On 4 Task 2)
        sa.UniqueConstraint("student_id", "course_id", name="uq_enrollment_student_course"),
    )

    # 5. professors — FK → departments
    op.create_table(
        "professors",
        sa.Column("professor_id",  sa.Integer(),    primary_key=True, autoincrement=True),
        sa.Column("prof_name",     sa.String(100),  nullable=False),
        sa.Column("email",         sa.String(100),  unique=True),
        sa.Column("department_id", sa.Integer(),    sa.ForeignKey("departments.department_id")),
        sa.Column("salary",        sa.Numeric(10, 2)),
    )


def downgrade() -> None:
    """
    Drop all tables in reverse creation order to respect foreign key constraints.
    """
    op.drop_table("professors")
    op.drop_table("enrollments")
    op.drop_table("courses")
    op.drop_table("students")
    op.drop_table("departments")
