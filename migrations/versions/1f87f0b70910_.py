"""empty message

Revision ID: 1f87f0b70910
Revises: 6199751722dd
Create Date: 2024-09-26 08:22:31.731389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1f87f0b70910'
down_revision: Union[str, None] = '6199751722dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('notes', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('notes', 'create_date')
    op.drop_column('notes', 'last_change_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('last_change_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('notes', sa.Column('create_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('notes', 'updated_at')
    op.drop_column('notes', 'created_at')
    # ### end Alembic commands ###
