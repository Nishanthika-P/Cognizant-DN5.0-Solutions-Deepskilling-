from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# ── Revision identifiers ──────────────────────────────────────────────────────
revision: str = "b2c3d4e5f6a1"
down_revision: Union[str, None] = "a1b2c3d4e5f6"   # points to migration 1
branch_labels: Union[str, Sequence[str], None] = None
depends_on:    Union[str, Sequence[str], None] = None
# ─────────────────────────────────────────────────────────────────────────────


def upgrade() -> None:
    """
    Add is_active column to students.
    server_default="true" back-fills existing rows so no NOT NULL violation occurs.
    """
    op.add_column(
        "students",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),  
        ),
    )


def downgrade() -> None:
    
    op.drop_column("students", "is_active")
