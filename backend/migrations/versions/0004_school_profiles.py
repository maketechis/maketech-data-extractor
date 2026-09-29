"""school profiles
Revision ID: 0004_school_profiles
Revises: 0003_integrity_constraints
"""
from alembic import op
import sqlalchemy as sa
revision="0004_school_profiles"; down_revision="0003_integrity_constraints"; branch_labels=None; depends_on=None
def upgrade():
    op.create_table("school_profiles",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("entity_id",sa.Integer(),sa.ForeignKey("entities.id",ondelete="CASCADE"),nullable=False),
        sa.Column("udise_code",sa.String(20),nullable=True),sa.Column("block",sa.String(160),nullable=True),
        sa.Column("village_town",sa.String(200),nullable=True),sa.Column("management",sa.String(160),nullable=True),
        sa.Column("category",sa.String(160),nullable=True),sa.Column("board",sa.String(120),nullable=True),
        sa.Column("attributes_json",sa.Text(),nullable=True),
        sa.UniqueConstraint("entity_id"),sa.UniqueConstraint("udise_code",name="uq_school_profiles_udise_code"))
    op.create_index("ix_school_profiles_entity_id","school_profiles",["entity_id"],unique=True)
    op.create_index("ix_school_profiles_udise_code","school_profiles",["udise_code"])
    op.create_index("ix_school_profiles_block","school_profiles",["block"])
def downgrade():
    op.drop_table("school_profiles")
