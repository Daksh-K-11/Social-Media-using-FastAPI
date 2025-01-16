"""add content column to post table

Revision ID: cf6d9f463f09
Revises: ddd8f8f5711f
Create Date: 2025-01-03 15:33:07.636486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf6d9f463f09'
down_revision: Union[str, None] = 'ddd8f8f5711f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     op.add_column('posts', sa.Column('content',sa.Integer(), nullable=False))
#     pass

def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
