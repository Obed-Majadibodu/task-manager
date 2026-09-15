"""create tasks table

Revision ID: 0081cbcdb092
Revises: 
Create Date: 2026-09-15 09:16:23.226483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0081cbcdb092'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        op.f("ix_tasks_id"),
        "tasks",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_tasks_id"),
        table_name="tasks"
    )

    op.drop_table("tasks")

