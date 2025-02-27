"""Initial migration

Revision ID: c0adef449ac2
Revises:
Create Date: 2025-02-26 17:15:01.253841

"""
from typing import Sequence, Union
import sqlmodel

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0adef449ac2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('charts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('query', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('flowstates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stage', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('query', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('chart', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['state_id'], ['flowstates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('flowstates')
    op.drop_table('charts')
    op.drop_table('users')
    # ### end Alembic commands ###
