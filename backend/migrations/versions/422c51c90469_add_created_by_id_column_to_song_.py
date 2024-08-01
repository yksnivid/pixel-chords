"""Add created_by_id column to Song without nullable

Revision ID: 422c51c90469
Revises: 550594b286ff
Create Date: 2024-08-01 14:08:16.790994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '422c51c90469'
down_revision = '550594b286ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.alter_column('lyrics',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('created_by_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('songs', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('created_by_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('lyrics',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###
