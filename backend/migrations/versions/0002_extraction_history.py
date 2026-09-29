"""extraction history
Revision ID: 0002_extraction_history
Revises: 0001_initial_core
"""
from alembic import op
import sqlalchemy as sa
revision="0002_extraction_history"; down_revision="0001_initial_core"; branch_labels=None; depends_on=None

def upgrade():
    op.create_table("extraction_runs",
        sa.Column("id",sa.Integer(),primary_key=True),sa.Column("campaign_id",sa.Integer(),sa.ForeignKey("campaigns.id",ondelete="SET NULL"),nullable=True),
        sa.Column("district_id",sa.Integer(),sa.ForeignKey("districts.id",ondelete="SET NULL"),nullable=True),sa.Column("run_type",sa.String(40),nullable=False),
        sa.Column("status",sa.String(30),nullable=False),sa.Column("started_at",sa.DateTime(timezone=True),nullable=False),sa.Column("completed_at",sa.DateTime(timezone=True),nullable=True),
        sa.Column("raw_count",sa.Integer(),nullable=False),sa.Column("saved_count",sa.Integer(),nullable=False),sa.Column("error",sa.Text(),nullable=True))
    for n in ("campaign_id","district_id","run_type","status"): op.create_index("ix_extraction_runs_"+n,"extraction_runs",[n])
    op.create_table("extraction_events",
        sa.Column("id",sa.Integer(),primary_key=True),sa.Column("run_id",sa.Integer(),sa.ForeignKey("extraction_runs.id",ondelete="CASCADE"),nullable=False),
        sa.Column("entity_id",sa.Integer(),sa.ForeignKey("entities.id",ondelete="SET NULL"),nullable=True),sa.Column("event_type",sa.String(50),nullable=False),
        sa.Column("field_name",sa.String(50),nullable=True),sa.Column("old_value",sa.Text(),nullable=True),sa.Column("new_value",sa.Text(),nullable=True),
        sa.Column("source_url",sa.Text(),nullable=True),sa.Column("confidence",sa.String(20),nullable=True),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
    for n in ("run_id","entity_id","event_type","field_name","created_at"): op.create_index("ix_extraction_events_"+n,"extraction_events",[n])

def downgrade():
    op.drop_table("extraction_events"); op.drop_table("extraction_runs")
