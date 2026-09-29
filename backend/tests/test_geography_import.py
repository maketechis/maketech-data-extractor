from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Country, District, State
from app.services.geography_import import import_india_geography

def test_geography_import_is_idempotent(tmp_path: Path):
    csv=tmp_path/"geo.csv"
    csv.write_text("state_name,state_code,district_name\nBihar,BR,Siwan\nBihar,BR,Patna\n",encoding="utf-8")
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        first=import_india_geography(db,csv); second=import_india_geography(db,csv)
        assert first=={"states_created":1,"districts_created":2}
        assert second=={"states_created":0,"districts_created":0}
        assert len(db.scalars(select(State)).all())==1
        assert len(db.scalars(select(District)).all())==2
        assert db.scalar(select(Country).where(Country.iso_code=="IN")).name=="India"
