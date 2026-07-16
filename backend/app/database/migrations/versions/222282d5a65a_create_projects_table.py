"""create projects table

Revision ID: 222282d5a65a
Revises: 9dab418ee283
Create Date: 2026-07-16 12:05:35.663897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '222282d5a65a'
down_revision = '9dab418ee283'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('projects')
