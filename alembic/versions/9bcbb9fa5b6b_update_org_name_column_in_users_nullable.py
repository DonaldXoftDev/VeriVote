"""update org_name column in users nullable

Revision ID: 9bcbb9fa5b6b
Revises: 33429e9287ee
Create Date: 2026-11-26 05:50:54.226380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bcbb9fa5b6b'
down_revision: Union[str, None] = '33429e9287ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column(
            'org_name',
            existing_type= sa.String(length=150),
            nullable=True
        )


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column(
            'org_name',
            existing_type=sa.String(length=150),
            nullable=False,
        )
