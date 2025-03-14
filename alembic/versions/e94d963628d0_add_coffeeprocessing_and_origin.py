"""Add CoffeeProcessing and Origin

Revision ID: e94d963628d0
Revises: bbcb34493cc7
Create Date: 2025-03-14 22:41:23.403462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.db.models import Origin, CoffeeProcessing

# revision identifiers, used by Alembic.
revision: str = 'e94d963628d0'
down_revision: Union[str, None] = 'bbcb34493cc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Удаляем старый столбец
    op.drop_column('coffees', 'origin')

    # Создаем новый тип Enum
    origin_enum = postgresql.ENUM(Origin, name="origin_enum")
    origin_enum.create(op.get_bind(), checkfirst=True)

    # Создаем новый столбец с типом Enum
    op.add_column(
        'coffees',
        sa.Column('origin', origin_enum, nullable=True)  # или nullable=False, если нужно
    )

    # Удаляем старый столбец
    op.drop_column('coffees', 'processing')

    # Создаем новый тип Enum
    processing_enum = postgresql.ENUM(CoffeeProcessing, name="processing_enum")
    processing_enum.create(op.get_bind(), checkfirst=True)

    # Создаем новый столбец с типом Enum
    op.add_column(
        'coffees',
        sa.Column('processing', processing_enum, nullable=True)  # или nullable=False, если нужно
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
