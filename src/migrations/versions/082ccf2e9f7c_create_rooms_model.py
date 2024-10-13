"""Create rooms model

Revision ID: 082ccf2e9f7c
Revises: e3eaf1f49221
Create Date: 2024-10-13 19:58:33.484353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '082ccf2e9f7c'
down_revision: Union[str, None] = 'e3eaf1f49221'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
            op.create_table('rooms',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('hotel_id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('price', sa.Integer(), nullable=False),
            sa.Column('quantity', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
            sa.PrimaryKeyConstraint('id')
            )


def downgrade() -> None:
            op.drop_table('rooms')
