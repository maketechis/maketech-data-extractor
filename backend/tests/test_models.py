from app.database import Base
from app import models  # noqa: F401

def test_core_tables_registered():
    expected={"countries","states","districts","entity_types","entities","entity_contacts","entity_websites","entity_sources","campaigns","campaign_locations"}
    assert expected.issubset(set(Base.metadata.tables))
