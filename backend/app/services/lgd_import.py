import csv
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Country,District,State
from app.services.geography_import import normalize_name

def _value(row,*names):
    lowered={str(k).strip().lower():str(v or "").strip() for k,v in row.items()}
    for name in names:
        value=lowered.get(name.lower())
        if value: return value
    return None

def import_lgd_states(db:Session,path:str|Path):
    india=db.scalar(select(Country).where(Country.iso_code=="IN"))
    if not india: india=Country(name="India",iso_code="IN"); db.add(india); db.flush()
    created=updated=skipped=0
    with Path(path).open(newline="",encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            code=_value(row,"state code","state_code","lgd_state_code"); name=_value(row,"state name (in english)","state name","state_name")
            if not code or not name: skipped+=1; continue
            state=db.scalar(select(State).where(State.lgd_code==code)) or db.scalar(select(State).where(State.country_id==india.id,State.name==name))
            if state: state.name=name; state.lgd_code=code; updated+=1
            else: db.add(State(country_id=india.id,name=name,lgd_code=code)); created+=1
    db.commit(); return {"created":created,"updated":updated,"skipped":skipped}

def import_lgd_districts(db:Session,path:str|Path):
    india=db.scalar(select(Country).where(Country.iso_code=="IN")); created=updated=skipped=0
    if not india: raise ValueError("Import LGD states first")
    with Path(path).open(newline="",encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            code=_value(row,"district code","district_code","lgd_district_code"); name=_value(row,"district name (in english)","district name","district_name")
            state_code=_value(row,"state code","state_code","lgd_state_code")
            state=db.scalar(select(State).where(State.country_id==india.id,State.lgd_code==state_code)) if state_code else None
            if not code or not name or not state: skipped+=1; continue
            district=db.scalar(select(District).where(District.lgd_code==code)) or db.scalar(select(District).where(District.state_id==state.id,District.name==name))
            if district: district.name=name; district.normalized_name=normalize_name(name); district.lgd_code=code; updated+=1
            else: db.add(District(state_id=state.id,name=name,normalized_name=normalize_name(name),lgd_code=code)); created+=1
    db.commit(); return {"created":created,"updated":updated,"skipped":skipped}
