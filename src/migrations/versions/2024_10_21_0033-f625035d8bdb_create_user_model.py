"""Create user model

Revision ID: f625035d8bdb
Revises: 990410d986a8
Create Date: 2024-10-21 00:33:27.081248

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f625035d8bdb"
down_revision: Union[str, None] = "990410d986a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
