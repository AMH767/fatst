"""add content column to posts table

Revision ID: 818a12cdeb58
Revises: 17fd73caa25d
Create Date: 2023-01-02 14:33:14.476671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '818a12cdeb58'
down_revision = '17fd73caa25d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
