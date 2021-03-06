"""empty message

Revision ID: 78630380ac81
Revises: fd023fc5fabe
Create Date: 2017-10-21 20:04:46.319229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78630380ac81'
down_revision = 'fd023fc5fabe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('modification_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'modification_date')
    # ### end Alembic commands ###
