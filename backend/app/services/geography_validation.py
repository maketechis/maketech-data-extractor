from collections import Counter
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Country,District,State

def validate_india_geography(db:Session)->dict:
    errors=[]; warnings=[]
    india=db.scalar(select(Country).where(Country.iso_code=="IN"))
    if not india:
        return {"valid":False,"errors":["India (IN) is missing"],"warnings":[],"states":0,"districts":0}
    states=db.scalars(select(State).where(State.country_id==india.id)).all()
    districts=db.scalars(select(District).join(State,District.state_id==State.id).where(State.country_id==india.id)).all()
    if not states: errors.append("No India states/UTs imported")
    if not districts: errors.append("No India districts imported")
    state_codes=[x.lgd_code for x in states if x.lgd_code]
    district_codes=[x.lgd_code for x in districts if x.lgd_code]
    if len(state_codes)!=len(states): errors.append("One or more states/UTs are missing LGD codes")
    if len(district_codes)!=len(districts): errors.append("One or more districts are missing LGD codes")
    if any(v>1 for v in Counter(state_codes).values()): errors.append("Duplicate state/UT LGD codes")
    if any(v>1 for v in Counter(district_codes).values()): errors.append("Duplicate district LGD codes")
    pairs=[(x.state_id,x.normalized_name) for x in districts]
    if any(v>1 for v in Counter(pairs).values()): errors.append("Duplicate normalized district names within a state")
    bihar=db.scalar(select(State).where(State.country_id==india.id,State.name=="Bihar"))
    if not bihar: errors.append("Bihar is missing")
    else:
        siwan=db.scalar(select(District).where(District.state_id==bihar.id,District.name=="Siwan"))
        if not siwan: errors.append("Bihar / Siwan is missing")
        elif not siwan.lgd_code: errors.append("Siwan is missing an LGD code")
    if len(states)<30: warnings.append("India state/UT count looks unexpectedly low")
    if len(districts)<700: warnings.append("India district count looks unexpectedly low; verify source/version")
    return {"valid":not errors,"errors":errors,"warnings":warnings,"states":len(states),"districts":len(districts)}
