from sqlalchemy import create_engine,func,select
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Country,EntityType
from app.services.bootstrap import bootstrap_core
def test_bootstrap_is_idempotent():
    engine=create_engine("sqlite:///:memory:");Base.metadata.create_all(engine)
    with Session(engine) as db:
        assert bootstrap_core(db)=={"countries":1,"entity_types":2}
        assert bootstrap_core(db)=={"countries":0,"entity_types":0}
        assert db.scalar(select(func.count(Country.id)))==1
        assert db.scalar(select(func.count(EntityType.id)))==2
