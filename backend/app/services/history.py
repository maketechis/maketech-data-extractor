from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.history import ExtractionEvent, ExtractionRun

def start_run(db:Session,*,campaign_id=None,district_id=None,run_type="collection"):
    row=ExtractionRun(campaign_id=campaign_id,district_id=district_id,run_type=run_type,status="running")
    db.add(row); db.commit(); db.refresh(row); return row

def finish_run(db:Session,run:ExtractionRun,*,status="completed",raw_count=0,saved_count=0,error=None):
    run.status=status; run.raw_count=raw_count; run.saved_count=saved_count; run.error=error
    run.completed_at=datetime.now(timezone.utc); db.commit(); return run

def record_event(db:Session,*,run_id,entity_id=None,event_type,field_name=None,old_value=None,new_value=None,source_url=None,confidence=None):
    row=ExtractionEvent(run_id=run_id,entity_id=entity_id,event_type=event_type,field_name=field_name,old_value=old_value,new_value=new_value,source_url=source_url,confidence=str(confidence) if confidence is not None else None)
    db.add(row); db.flush(); return row
