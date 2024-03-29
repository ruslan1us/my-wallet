"""Added foreign keys to expense, money-spinner, and income tables

Revision ID: df6ae1696892
Revises: 81c5d2e96a0e
Create Date: 2024-03-22 11:20:36.583453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df6ae1696892'
down_revision: Union[str, None] = '81c5d2e96a0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expense', sa.Column('user', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'expense', 'users', ['user'], ['id'])
    op.add_column('salary', sa.Column('user', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'salary', 'users', ['user'], ['id'])
    op.add_column('tip', sa.Column('user', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tip', 'users', ['user'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tip', type_='foreignkey')
    op.drop_column('tip', 'user')
    op.drop_constraint(None, 'salary', type_='foreignkey')
    op.drop_column('salary', 'user')
    op.drop_constraint(None, 'expense', type_='foreignkey')
    op.drop_column('expense', 'user')
    # ### end Alembic commands ###
