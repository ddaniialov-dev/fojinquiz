"""changed email field to username

Revision ID: 60b978c6fa58
Revises: 60cb7bffea0d
Create Date: 2022-02-28 09:49:46.908557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60b978c6fa58'
down_revision = '60cb7bffea0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.drop_column('users', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.drop_column('users', 'username')
    # ### end Alembic commands ###