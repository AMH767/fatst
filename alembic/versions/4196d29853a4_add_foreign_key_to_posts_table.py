"""add foreign-key to posts table

Revision ID: 4196d29853a4
Revises: 7d8c2c8b79f1
Create Date: 2023-01-02 14:58:22.215629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4196d29853a4'
down_revision = '7d8c2c8b79f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", 'posts')
    op.drop_column("posts", "owner_id")
    pass
