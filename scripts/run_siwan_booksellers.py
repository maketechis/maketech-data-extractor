from sqlalchemy import select
from app.collector.adapters.osm_overpass import OSMOverpassAdapter
from app.collector.engine import CollectorEngine
from app.database import SessionLocal
from app.models.core import Country, District, EntityType, State
from app.services.bootstrap import ensure_development_seed

with SessionLocal() as db:
    ids=ensure_development_seed(db)
    result=CollectorEngine([OSMOverpassAdapter()]).collect(
        db=db,
        entity_type=db.get(EntityType,ids["bookseller_type_id"]),
        country=db.get(Country,ids["country_id"]),
        state=db.get(State,ids["state_id"]),
        district=db.get(District,ids["district_id"]),
    )
    print(result)
