"""empty message

Revision ID: 62b6fc121636
Revises: cad036b3a370
Create Date: 2022-12-15 09:48:55.482648

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '62b6fc121636'
down_revision = 'cad036b3a370'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('img',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('pet_img')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pet_img',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('img', mysql.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('img')
    # ### end Alembic commands ###
