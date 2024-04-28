"""add fields to users table

Revision ID: 479267e21970
Revises: 1adbcbfced8c
Create Date: 2024-04-21 22:00:16.366682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '479267e21970'
down_revision = '1adbcbfced8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gender', sa.String(length=25), nullable=False, default=""))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('gender')

    # ### end Alembic commands ###
