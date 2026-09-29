"""LGD geography identifiers
Revision ID: 0005_lgd_codes
Revises: 0004_school_profiles
"""
from alembic import op
import sqlalchemy as sa
revision="0005_lgd_codes"; down_revision="0004_school_profiles"; branch_labels=None; depends_on=None
def upgrade():
    op.add_column("states",sa.Column("lgd_code",sa.String(20),nullable=True))
    op.add_column("districts",sa.Column("lgd_code",sa.String(20),nullable=True))
    op.create_unique_constraint("uq_states_lgd_code","states",["lgd_code"])
    op.create_unique_constraint("uq_districts_lgd_code","districts",["lgd_code"])
    op.create_index("ix_states_lgd_code","states",["lgd_code"])
    op.create_index("ix_districts_lgd_code","districts",["lgd_code"])
def downgrade():
    op.drop_index("ix_districts_lgd_code",table_name="districts"); op.drop_constraint("uq_districts_lgd_code","districts",type_="unique"); op.drop_column("districts","lgd_code")
    op.drop_index("ix_states_lgd_code",table_name="states"); op.drop_constraint("uq_states_lgd_code","states",type_="unique"); op.drop_column("states","lgd_code")
