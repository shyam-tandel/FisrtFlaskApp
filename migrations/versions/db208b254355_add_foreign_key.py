"""add foreign key

Revision ID: db208b254355
Revises: 2b3731e7acd6
Create Date: 2025-01-09 14:27:55.608352

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'db208b254355'
down_revision = '2b3731e7acd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.alter_column('category_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.create_foreign_key(None, 'category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('category_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
