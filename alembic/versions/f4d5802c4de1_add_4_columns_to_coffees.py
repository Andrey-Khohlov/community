"""Add 4 columns to coffees

Revision ID: f4d5802c4de1
Revises: 12b6b6f320cf
Create Date: 2025-03-08 14:13:41.790463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f4d5802c4de1'
down_revision: Union[str, None] = '12b6b6f320cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coffees', sa.Column('notes', sa.String(), nullable=True))
    op.add_column('coffees', sa.Column('importer', sa.String(length=256), nullable=True))
    op.add_column('coffees', sa.Column('subregion', sa.String(length=256), nullable=True))
    op.add_column('coffees', sa.Column('plant', sa.String(length=256), nullable=True))
    op.alter_column('coffees', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('coffees', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text("timezone('utc'::text, now())"))
    op.alter_column('coffees', 'exporter',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('coffees', 'exporter',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('coffees', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text("timezone('utc'::text, now())"))
    op.alter_column('coffees', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('coffees', 'plant')
    op.drop_column('coffees', 'subregion')
    op.drop_column('coffees', 'importer')
    op.drop_column('coffees', 'notes')
    # ### end Alembic commands ###
