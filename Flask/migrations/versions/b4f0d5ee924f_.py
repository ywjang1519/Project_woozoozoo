"""empty message

Revision ID: b4f0d5ee924f
Revises: 27ae9367d9c2
Create Date: 2022-12-20 13:10:14.456973

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b4f0d5ee924f'
down_revision = '27ae9367d9c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('img')
    with op.batch_alter_table('pet_img', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('img',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pet_img', schema=None) as batch_op:
        batch_op.alter_column('img',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False,
               autoincrement=True)

    op.create_table('img',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('img', mysql.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('answer')
    op.drop_table('question')
    # ### end Alembic commands ###
