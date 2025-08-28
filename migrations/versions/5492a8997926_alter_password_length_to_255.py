"""alter password length to 255

Revision ID: 5492a8997926
Revises: df09fbe42b11
Create Date: 2025-08-27 14:11:00.766936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5492a8997926'
down_revision: Union[str, Sequence[str], None] = 'df09fbe42b11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
