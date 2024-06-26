"""Made amount columns in tables not nullable. Added unique parameter for name in MoneySpinnerTable.

Revision ID: 261a00fb41d6
Revises: 152c33d238dc
Create Date: 2024-05-23 16:32:45.218041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '261a00fb41d6'
down_revision: Union[str, None] = '152c33d238dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('money_spinner_name_key', 'money_spinner', type_='unique')
    op.create_unique_constraint('uq_moneyspinner_name_owner', 'money_spinner', ['name', 'owner_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_moneyspinner_name_owner', 'money_spinner', type_='unique')
    op.create_unique_constraint('money_spinner_name_key', 'money_spinner', ['name'])
    # ### end Alembic commands ###
