"""truncate reviews table

Revision ID: bbcb34493cc7
Revises: 5f35828ddd95
Create Date: 2025-03-10 00:45:40.699254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbcb34493cc7'
down_revision: Union[str, None] = '5f35828ddd95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Очистка таблицы reviews
    op.execute("TRUNCATE TABLE reviews RESTART IDENTITY;")


def downgrade() -> None:
    """Downgrade schema."""
    # Откат не требуется, так как TRUNCATE необратим
    pass
