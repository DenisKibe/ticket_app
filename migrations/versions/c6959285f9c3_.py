"""empty message

Revision ID: c6959285f9c3
Revises: d9e1c3b953a1
Create Date: 2020-08-23 16:13:44.840584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6959285f9c3'
down_revision = 'd9e1c3b953a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('commentId', sa.String(length=20), nullable=False),
    sa.Column('user_id', sa.String(length=20), nullable=False),
    sa.Column('ticket_id', sa.String(length=20), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('comment_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.ticketId'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.userId'], ),
    sa.PrimaryKeyConstraint('commentId'),
    sa.UniqueConstraint('commentId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###