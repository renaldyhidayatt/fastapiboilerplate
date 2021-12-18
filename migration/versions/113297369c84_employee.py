"""employee

Revision ID: 113297369c84
Revises: 0f6c9f955f92
Create Date: 2021-12-19 02:56:20.458919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "113297369c84"
down_revision = "0f6c9f955f92"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "employee",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("jobs", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("employee")
