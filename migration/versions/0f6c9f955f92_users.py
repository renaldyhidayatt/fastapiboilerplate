"""users

Revision ID: 0f6c9f955f92
Revises: 
Create Date: 2021-12-19 02:55:56.933723

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "0f6c9f955f92"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("verifyCationToken", sa.String(), nullable=True),
        sa.Column("verifyDate", sa.DateTime(), nullable=True),
        sa.Column('passwordResetDate', sa.DateTime(), nullable=True),
        sa.Column('resetPasswordToken', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("users")
