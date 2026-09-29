from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Country, District, EntityType, State
from app.services.bootstrap import ensure_development_seed

def test_development_seed_is_idempotent():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        a=ensure_development_seed(db); b=ensure_development_seed(db)
        assert a==b
        assert len(db.scalars(select(Country)).all())==1
        assert len(db.scalars(select(State)).all())==1
        assert len(db.scalars(select(District)).all())==1
        assert {x.slug for x in db.scalars(select(EntityType)).all()}=={"bookseller","school"}
