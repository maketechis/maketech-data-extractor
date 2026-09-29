from sqlalchemy import create_engine,select
from sqlalchemy.orm import Session
from app.database import Base
from app.models.history import ExtractionEvent
from app.services.history import finish_run,record_event,start_run

def test_history_run_and_event():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        run=start_run(db,run_type="collection")
        record_event(db,run_id=run.id,event_type="field_added",field_name="email",new_value="info@example.com",source_url="https://example.com/contact",confidence=.9)
        db.commit(); finish_run(db,run,raw_count=10,saved_count=8)
        assert run.status=="completed" and run.raw_count==10
        event=db.scalar(select(ExtractionEvent))
        assert event.new_value=="info@example.com"
