"""integrity constraints
Revision ID: 0003_integrity_constraints
Revises: 0002_campaign_history
"""
from alembic import op
import sqlalchemy as sa
revision="0003_integrity_constraints"; down_revision="0002_campaign_history"; branch_labels=None; depends_on=None

def upgrade():
    op.create_unique_constraint("uq_entity_contact","entity_contacts",["entity_id","contact_type","value"])
    op.create_unique_constraint("uq_entity_website_domain","entity_websites",["entity_id","domain"])
    op.create_unique_constraint("uq_campaign_run_district","campaign_run_districts",["campaign_run_id","district_id"])

def downgrade():
    op.drop_constraint("uq_campaign_run_district","campaign_run_districts",type_="unique")
    op.drop_constraint("uq_entity_website_domain","entity_websites",type_="unique")
    op.drop_constraint("uq_entity_contact","entity_contacts",type_="unique")
