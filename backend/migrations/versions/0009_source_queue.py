"""source queue
Revision ID: 0009_source_queue
Revises: 0008_campaign_quality
"""
from alembic import op
import sqlalchemy as sa
revision="0009_source_queue";down_revision="0008_campaign_quality";branch_labels=None;depends_on=None
def upgrade():
    op.create_table("campaign_sources",sa.Column("id",sa.Integer(),primary_key=True),sa.Column("campaign_id",sa.Integer(),sa.ForeignKey("campaigns.id",ondelete="CASCADE"),nullable=False),sa.Column("district_id",sa.Integer(),sa.ForeignKey("districts.id"),nullable=False),sa.Column("engine",sa.String(30),nullable=False),sa.Column("query",sa.Text(),nullable=False),sa.Column("page_number",sa.Integer(),nullable=False),sa.Column("rank",sa.Integer(),nullable=False),sa.Column("title",sa.Text(),nullable=False),sa.Column("url",sa.Text(),nullable=False),sa.Column("status",sa.String(30),nullable=False,server_default="pending"),sa.Column("records_raw",sa.Integer(),nullable=False,server_default="0"),sa.Column("records_accepted",sa.Integer(),nullable=False,server_default="0"),sa.Column("records_saved",sa.Integer(),nullable=False,server_default="0"),sa.Column("last_error",sa.Text(),nullable=True),sa.UniqueConstraint("campaign_id","url",name="uq_campaign_source_url"))
    op.create_index("ix_campaign_sources_campaign","campaign_sources",["campaign_id"])
def downgrade():op.drop_table("campaign_sources")
