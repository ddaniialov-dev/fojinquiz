"""added relations for questions and sessions

Revision ID: b2e9c88a3056
Revises: 40a1d6dfdd83
Create Date: 2022-03-22 14:35:03.676320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2e9c88a3056'
down_revision = '40a1d6dfdd83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session_question',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('association')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association',
    sa.Column('question_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('session_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], name='association_question_id_fkey'),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], name='association_session_id_fkey')
    )
    op.drop_table('session_question')
    # ### end Alembic commands ###