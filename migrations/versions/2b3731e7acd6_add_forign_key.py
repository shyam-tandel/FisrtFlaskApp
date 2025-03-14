"""add forign key.

Revision ID: 2b3731e7acd6
Revises: 
Create Date: 2025-01-09 13:30:58.625224

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2b3731e7acd6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.alter_column('category_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.alter_column('category_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
