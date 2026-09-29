"""initial core schema

Revision ID: 0001_initial_core
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_core"
down_revision = None
branch_labels = None
depends_on = None

campaign_status = sa.Enum("DRAFT","QUEUED","RUNNING","PAUSED","COMPLETED","FAILED","CANCELLED", name="campaignstatus")
location_status = sa.Enum("PENDING","RUNNING","COLLECTING","ENRICHING","REVIEW","COMPLETED","FAILED", name="locationstatus")

def upgrade():
    op.create_table("countries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("iso_code", sa.String(2), nullable=False),
        sa.UniqueConstraint("name"), sa.UniqueConstraint("iso_code"))
    op.create_index("ix_countries_name","countries",["name"])
    op.create_table("entity_types",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("slug", sa.String(120), nullable=False),
        sa.Column("config_json", sa.Text(), nullable=True),
        sa.UniqueConstraint("name"), sa.UniqueConstraint("slug"))
    op.create_index("ix_entity_types_slug","entity_types",["slug"])
    op.create_table("states",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("country_id", sa.Integer(), sa.ForeignKey("countries.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("code", sa.String(20), nullable=True),
        sa.UniqueConstraint("country_id","name"))
    op.create_index("ix_states_country_id","states",["country_id"]); op.create_index("ix_states_name","states",["name"])
    op.create_table("districts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("state_id", sa.Integer(), sa.ForeignKey("states.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("normalized_name", sa.String(160), nullable=False),
        sa.UniqueConstraint("state_id","name"))
    op.create_index("ix_districts_state_id","districts",["state_id"]); op.create_index("ix_districts_name","districts",["name"]); op.create_index("ix_districts_normalized_name","districts",["normalized_name"])
    op.create_table("entities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entity_type_id", sa.Integer(), sa.ForeignKey("entity_types.id"), nullable=False),
        sa.Column("name", sa.String(300), nullable=False), sa.Column("normalized_name", sa.String(300), nullable=False),
        sa.Column("country_id", sa.Integer(), sa.ForeignKey("countries.id"), nullable=False),
        sa.Column("state_id", sa.Integer(), sa.ForeignKey("states.id"), nullable=True),
        sa.Column("district_id", sa.Integer(), sa.ForeignKey("districts.id"), nullable=True),
        sa.Column("address", sa.Text(), nullable=True), sa.Column("pin", sa.String(20), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True), sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("status", sa.String(40), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    for n in ["entity_type_id","name","normalized_name","country_id","state_id","district_id","pin"]: op.create_index("ix_entities_"+n,"entities",[n])
    op.create_table("campaigns",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(200), nullable=False),
        sa.Column("entity_type_id", sa.Integer(), sa.ForeignKey("entity_types.id"), nullable=False),
        sa.Column("country_id", sa.Integer(), sa.ForeignKey("countries.id"), nullable=False),
        sa.Column("collection_level", sa.String(30), nullable=False), sa.Column("status", campaign_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    for n in ["entity_type_id","country_id","status"]: op.create_index("ix_campaigns_"+n,"campaigns",[n])
    op.create_table("entity_contacts",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("entity_id", sa.Integer(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("contact_type", sa.String(30), nullable=False), sa.Column("value", sa.String(500), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True), sa.Column("confidence", sa.Float(), nullable=True), sa.Column("verified", sa.Boolean(), nullable=False))
    op.create_index("ix_entity_contacts_entity_id","entity_contacts",["entity_id"]); op.create_index("ix_entity_contacts_contact_type","entity_contacts",["contact_type"])
    op.create_table("entity_websites",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("entity_id", sa.Integer(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("url", sa.Text(), nullable=False), sa.Column("domain", sa.String(255), nullable=False), sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("verification_status", sa.String(40), nullable=False))
    op.create_index("ix_entity_websites_entity_id","entity_websites",["entity_id"]); op.create_index("ix_entity_websites_domain","entity_websites",["domain"])
    op.create_table("entity_sources",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("entity_id", sa.Integer(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_type", sa.String(80), nullable=False), sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("source_record_id", sa.String(255), nullable=True), sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_entity_sources_entity_id","entity_sources",["entity_id"]); op.create_index("ix_entity_sources_source_type","entity_sources",["source_type"])
    op.create_table("campaign_locations",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("campaign_id", sa.Integer(), sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False),
        sa.Column("state_id", sa.Integer(), sa.ForeignKey("states.id"), nullable=False), sa.Column("district_id", sa.Integer(), sa.ForeignKey("districts.id"), nullable=False),
        sa.Column("status", location_status, nullable=False), sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("records_found", sa.Integer(), nullable=False), sa.Column("records_saved", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True), sa.Column("started_at", sa.DateTime(timezone=True), nullable=True), sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("campaign_id","district_id"))
    for n in ["campaign_id","state_id","district_id","status"]: op.create_index("ix_campaign_locations_"+n,"campaign_locations",[n])

def downgrade():
    op.drop_table("campaign_locations"); op.drop_table("entity_sources"); op.drop_table("entity_websites"); op.drop_table("entity_contacts")
    op.drop_table("campaigns"); op.drop_table("entities"); op.drop_table("districts"); op.drop_table("states"); op.drop_table("entity_types"); op.drop_table("countries")
    location_status.drop(op.get_bind(), checkfirst=True); campaign_status.drop(op.get_bind(), checkfirst=True)
