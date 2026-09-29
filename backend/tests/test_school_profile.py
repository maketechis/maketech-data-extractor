from sqlalchemy import create_engine
from app.database import Base
from app import models
from app.models.school import SchoolProfile

def test_school_profile_table_registered():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    assert "school_profiles" in Base.metadata.tables
