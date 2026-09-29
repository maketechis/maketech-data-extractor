import csv
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Country, District, State

def normalize_name(value: str) -> str:
    return " ".join(value.strip().lower().split())

def import_india_geography(db: Session, csv_path: str | Path) -> dict:
    path=Path(csv_path)
    country=db.scalar(select(Country).where(Country.iso_code=="IN"))
    if not country:
        country=Country(name="India",iso_code="IN"); db.add(country); db.flush()
    states_created=districts_created=0
    state_cache={}
    with path.open(newline="",encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            state_name=row["state_name"].strip(); district_name=row["district_name"].strip()
            if not state_name or not district_name: continue
            key=normalize_name(state_name)
            state=state_cache.get(key)
            if not state:
                state=db.scalar(select(State).where(State.country_id==country.id, State.name==state_name))
                if not state:
                    state=State(country_id=country.id,name=state_name,code=(row.get("state_code") or "").strip() or None)
                    db.add(state); db.flush(); states_created+=1
                state_cache[key]=state
            exists=db.scalar(select(District.id).where(District.state_id==state.id, District.name==district_name))
            if not exists:
                db.add(District(state_id=state.id,name=district_name,normalized_name=normalize_name(district_name))); districts_created+=1
    db.commit()
    return {"states_created":states_created,"districts_created":districts_created}
