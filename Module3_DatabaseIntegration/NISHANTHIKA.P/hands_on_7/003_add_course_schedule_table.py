from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

 
revision: str = "c3d4e5f6a1b2"
down_revision: Union[str, None] = "b2c3d4e5f6a1"  
branch_labels: Union[str, Sequence[str], None] = None
depends_on:    Union[str, Sequence[str], None] = None


def upgrade() -> None:
   
    op.create_table(
        "course_schedules",
        sa.Column("schedule_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("courses.course_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("day_of_week", sa.String(10), nullable=False),   
        sa.Column("start_time",  sa.Time(),      nullable=False),
        sa.Column("end_time",    sa.Time(),      nullable=False),
    )

    
    op.create_index(
        "ix_course_schedules_course_id",
        "course_schedules",
        ["course_id"],
    )


def downgrade() -> None:
    
    op.drop_index("ix_course_schedules_course_id", table_name="course_schedules")
    op.drop_table("course_schedules")
