"""campaign quality
Revision ID: 0008_campaign_quality
Revises: 0007_campaign_search_settings
"""
from alembic import op
import sqlalchemy as sa
revision="0008_campaign_quality";down_revision="0007_campaign_search_settings";branch_labels=None;depends_on=None
def upgrade():
    op.add_column("campaigns",sa.Column("quality_status",sa.String(30),nullable=False,server_default="unknown"))
    op.add_column("campaigns",sa.Column("quality_json",sa.Text(),nullable=True))
def downgrade():
    op.drop_column("campaigns","quality_json");op.drop_column("campaigns","quality_status")
