import csv
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.collector.normalizer import normalize_name
from app.models.core import Country,District,Entity,EntityType,State
from app.models.school import SchoolProfile

def import_schools(db:Session,path:str|Path)->dict:
    created=updated=skipped=0
    with Path(path).open(newline="",encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            udise=(row.get("udise_code") or "").strip() or None
            name=(row.get("school_name") or "").strip()
            state_name=(row.get("state") or "").strip(); district_name=(row.get("district") or "").strip()
            if not name or not state_name or not district_name: skipped+=1; continue
            country=db.scalar(select(Country).where(Country.iso_code=="IN"))
            et=db.scalar(select(EntityType).where(EntityType.slug=="school"))
            state=db.scalar(select(State).where(State.country_id==country.id,State.name==state_name)) if country else None
            district=db.scalar(select(District).where(District.state_id==state.id,District.name==district_name)) if state else None
            if not all((country,et,state,district)): skipped+=1; continue
            profile=db.scalar(select(SchoolProfile).where(SchoolProfile.udise_code==udise)) if udise else None
            if profile:
                entity=db.get(Entity,profile.entity_id); updated+=1
            else:
                entity=Entity(entity_type_id=et.id,name=name,normalized_name=normalize_name(name),country_id=country.id,state_id=state.id,district_id=district.id,address=(row.get("address") or "").strip() or None,pin=(row.get("pin") or "").strip() or None)
                db.add(entity); db.flush(); profile=SchoolProfile(entity_id=entity.id,udise_code=udise); db.add(profile); created+=1
            profile.block=(row.get("block") or "").strip() or None
            profile.village_town=(row.get("village_town") or "").strip() or None
            profile.management=(row.get("management") or "").strip() or None
            profile.category=(row.get("category") or "").strip() or None
            profile.board=(row.get("board") or "").strip() or None
    db.commit(); return {"created":created,"updated":updated,"skipped":skipped}
