"""empty message

Revision ID: 612cb7862395
Revises: 9336b2f5a1c7
Create Date: 2016-04-18 20:07:41.402402

"""

# revision identifiers, used by Alembic.
revision = '612cb7862395'
down_revision = '9336b2f5a1c7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('aging_effects', sa.Column('age', sa.String(length=20), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('aging_effects', 'age')
    ### end Alembic commands ###
