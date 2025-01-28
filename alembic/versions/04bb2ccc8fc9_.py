"""empty message

Revision ID: 04bb2ccc8fc9
Revises: 168b34a39766
Create Date: 2025-01-25 23:34:35.979860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04bb2ccc8fc9'
down_revision: Union[str, None] = '168b34a39766'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_access_logs_id'), 'access_logs', ['id'], unique=False)
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_table('review_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.String(length=255), nullable=False),
    sa.Column('tone', sa.String(length=255), nullable=True),
    sa.Column('sentiment', sa.String(length=255), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_history_id'), 'review_history', ['id'], unique=False)
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=128), nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.drop_index(op.f('ix_review_history_id'), table_name='review_history')
    op.drop_table('review_history')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    op.drop_index(op.f('ix_access_logs_id'), table_name='access_logs')
    op.drop_table('access_logs')
    # ### end Alembic commands ###
