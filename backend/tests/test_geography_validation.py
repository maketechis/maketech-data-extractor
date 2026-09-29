from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Country,District,State
from app.services.geography_validation import validate_india_geography

def test_validation_confirms_siwan_but_warns_for_sample():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); db.add(c); db.flush()
        s=State(country_id=c.id,name="Bihar",lgd_code="10"); db.add(s); db.flush()
        db.add(District(state_id=s.id,name="Siwan",normalized_name="siwan",lgd_code="216")); db.commit()
        result=validate_india_geography(db)
        assert result["valid"] is True
        assert result["states"]==1 and result["districts"]==1
        assert result["warnings"]
