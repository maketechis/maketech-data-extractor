"""campaign history
Revision ID: 0002_campaign_history
Revises: 0001_initial_core
"""
from alembic import op
import sqlalchemy as sa
revision="0002_campaign_history"; down_revision="0001_initial_core"; branch_labels=None; depends_on=None

def upgrade():
    op.create_table("campaign_runs",
        sa.Column("id",sa.Integer(),primary_key=True),sa.Column("campaign_id",sa.Integer(),sa.ForeignKey("campaigns.id",ondelete="CASCADE"),nullable=False),
        sa.Column("status",sa.String(30),nullable=False),sa.Column("started_at",sa.DateTime(timezone=True),nullable=False),sa.Column("completed_at",sa.DateTime(timezone=True),nullable=True),
        sa.Column("districts_total",sa.Integer(),nullable=False),sa.Column("districts_completed",sa.Integer(),nullable=False),sa.Column("districts_failed",sa.Integer(),nullable=False),
        sa.Column("records_found",sa.Integer(),nullable=False),sa.Column("records_saved",sa.Integer(),nullable=False),sa.Column("notes",sa.Text(),nullable=True))
    for n in ("campaign_id","status","started_at"): op.create_index("ix_campaign_runs_"+n,"campaign_runs",[n])
    op.create_table("campaign_run_districts",
        sa.Column("id",sa.Integer(),primary_key=True),sa.Column("campaign_run_id",sa.Integer(),sa.ForeignKey("campaign_runs.id",ondelete="CASCADE"),nullable=False),
        sa.Column("district_id",sa.Integer(),sa.ForeignKey("districts.id",ondelete="RESTRICT"),nullable=False),sa.Column("status",sa.String(30),nullable=False),
        sa.Column("attempts",sa.Integer(),nullable=False),sa.Column("records_found",sa.Integer(),nullable=False),sa.Column("records_saved",sa.Integer(),nullable=False),
        sa.Column("started_at",sa.DateTime(timezone=True),nullable=True),sa.Column("completed_at",sa.DateTime(timezone=True),nullable=True),sa.Column("last_error",sa.Text(),nullable=True))
    for n in ("campaign_run_id","district_id","status"): op.create_index("ix_campaign_run_districts_"+n,"campaign_run_districts",[n])

def downgrade():
    op.drop_table("campaign_run_districts"); op.drop_table("campaign_runs")
