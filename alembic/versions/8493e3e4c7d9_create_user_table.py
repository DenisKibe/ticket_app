"""create user table

Revision ID: 8493e3e4c7d9
Revises: 
Create Date: 2020-08-16 08:34:30.006991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8493e3e4c7d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('userId', sa.String(20), primary_key=True, nullable=False, unique=True),
        sa.Column('username', sa.String(80), nullable=False),
        sa.Column('email', sa.String(120), unique=True),
        sa.Column('role', sa.String(20)),
    )


def downgrade():
    op.drop_table('user')
