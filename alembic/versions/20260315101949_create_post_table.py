"""
Revision ID: 20260315101949
Revises: 
Create Date: 2026-03-15 10:19:49.511000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import enum

# revision identifiers, used by Alembic.
revision = '20260315101949'
down_revision = None
branch_labels = None
depends_on = None

class PostStatusEnum(sa.Enum):
    def __init__(self, *args, **kwargs):
        super().__init__('draft', 'published', 'archived', name='poststatus', **kwargs)

def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('author', sa.String(length=100), nullable=False),
        sa.Column('status', PostStatusEnum(), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('posts')
    PostStatusEnum().drop(op.get_bind(), checkfirst=False)
