"""Constraint email

Revision ID: 9395ced823cd
Revises: f625035d8bdb
Create Date: 2024-10-21 03:52:18.304698

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9395ced823cd"
down_revision: Union[str, None] = "f625035d8bdb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
