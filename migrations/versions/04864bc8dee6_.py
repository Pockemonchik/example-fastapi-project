"""empty message

Revision ID: 04864bc8dee6
Revises: 
Create Date: 2024-09-24 17:18:07.291208

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "04864bc8dee6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("header", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("create_date", sa.DateTime(), nullable=False),
        sa.Column("last_change_date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notes")
    # ### end Alembic commands ###
