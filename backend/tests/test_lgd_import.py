from pathlib import Path
from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import District,State
from app.services.lgd_import import import_lgd_districts,import_lgd_states

def test_lgd_import(tmp_path:Path):
    states=tmp_path/"states.csv"; districts=tmp_path/"districts.csv"
    states.write_text("State Code,State Name (In English)\n10,Bihar\n",encoding="utf-8")
    districts.write_text("District Code,District Name (In English),State Code\n216,Siwan,10\n",encoding="utf-8")
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        assert import_lgd_states(db,states)["created"]==1
        assert import_lgd_districts(db,districts)["created"]==1
        assert db.scalar(select(State).where(State.lgd_code=="10")).name=="Bihar"
        assert db.scalar(select(District).where(District.lgd_code=="216")).name=="Siwan"
