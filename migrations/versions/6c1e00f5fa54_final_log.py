"""final log

Revision ID: 6c1e00f5fa54
Revises: 1a8989b8388d
Create Date: 2024-06-28 11:18:07.103902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c1e00f5fa54'
down_revision = '1a8989b8388d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sequence', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('roomName', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('actionNature', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('actionType', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('userAnswer', sa.String(length=2048), nullable=True))
        batch_op.add_column(sa.Column('userError', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('logs', schema=None) as batch_op:
        batch_op.drop_column('userError')
        batch_op.drop_column('userAnswer')
        batch_op.drop_column('actionType')
        batch_op.drop_column('actionNature')
        batch_op.drop_column('roomName')
        batch_op.drop_column('sequence')

    # ### end Alembic commands ###
