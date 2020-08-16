"""create ticket table

Revision ID: 168e6e7a20d7
Revises: 8493e3e4c7d9
Create Date: 2020-08-16 09:31:52.951373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '168e6e7a20d7'
down_revision = '8493e3e4c7d9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ticket',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(20), nullable=False),
        sa.Column('ticketId', sa.String(20), primary_key=True,unique=True, nullable=False),
        sa.Column('status', sa.String(20)),
        sa.Column('image', sa.UnicodeText()),
        sa.Column('comment', sa.Unicode(200)),
        sa.Column('category', sa.String(30)),
        sa.Column('priority', sa.String(20)),
        sa.Column('subject', sa.String(50)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade():
    pass
