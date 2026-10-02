"""campaign search settings
Revision ID: 0007_campaign_search_settings
Revises: 0006_app_users
"""
from alembic import op
import sqlalchemy as sa
revision="0007_campaign_search_settings";down_revision="0006_app_users";branch_labels=None;depends_on=None
def upgrade():
    op.add_column("campaigns",sa.Column("search_google",sa.Boolean(),nullable=False,server_default=sa.true()))
    op.add_column("campaigns",sa.Column("search_bing",sa.Boolean(),nullable=False,server_default=sa.true()))
    op.add_column("campaigns",sa.Column("search_yahoo",sa.Boolean(),nullable=False,server_default=sa.true()))
    op.add_column("campaigns",sa.Column("search_mode",sa.String(20),nullable=False,server_default="fallback"))
def downgrade():
    for x in ("search_mode","search_yahoo","search_bing","search_google"):op.drop_column("campaigns",x)
