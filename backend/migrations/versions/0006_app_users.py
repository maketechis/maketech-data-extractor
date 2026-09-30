"""application users
Revision ID: 0006_app_users
Revises: 0005_lgd_codes
"""
from alembic import op
import sqlalchemy as sa
revision="0006_app_users";down_revision="0005_lgd_codes";branch_labels=None;depends_on=None
def upgrade():
    op.create_table("app_users",sa.Column("id",sa.Integer(),primary_key=True),sa.Column("email",sa.String(320),nullable=False),sa.Column("password_hash",sa.String(255),nullable=False),sa.Column("is_active",sa.Boolean(),nullable=False),sa.Column("is_admin",sa.Boolean(),nullable=False),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.UniqueConstraint("email"))
    op.create_index("ix_app_users_email","app_users",["email"],unique=True)
def downgrade():op.drop_table("app_users")
