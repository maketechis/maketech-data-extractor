from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

def utcnow(): return datetime.now(timezone.utc)

class ExtractionRun(Base):
    __tablename__="extraction_runs"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int|None]=mapped_column(ForeignKey("campaigns.id",ondelete="SET NULL"),nullable=True,index=True)
    district_id: Mapped[int|None]=mapped_column(ForeignKey("districts.id",ondelete="SET NULL"),nullable=True,index=True)
    run_type: Mapped[str]=mapped_column(String(40),index=True)
    status: Mapped[str]=mapped_column(String(30),index=True,default="running")
    started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
    completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    raw_count: Mapped[int]=mapped_column(Integer,default=0)
    saved_count: Mapped[int]=mapped_column(Integer,default=0)
    error: Mapped[str|None]=mapped_column(Text,nullable=True)

class ExtractionEvent(Base):
    __tablename__="extraction_events"
    id: Mapped[int]=mapped_column(primary_key=True)
    run_id: Mapped[int]=mapped_column(ForeignKey("extraction_runs.id",ondelete="CASCADE"),index=True)
    entity_id: Mapped[int|None]=mapped_column(ForeignKey("entities.id",ondelete="SET NULL"),nullable=True,index=True)
    event_type: Mapped[str]=mapped_column(String(50),index=True)
    field_name: Mapped[str|None]=mapped_column(String(50),nullable=True,index=True)
    old_value: Mapped[str|None]=mapped_column(Text,nullable=True)
    new_value: Mapped[str|None]=mapped_column(Text,nullable=True)
    source_url: Mapped[str|None]=mapped_column(Text,nullable=True)
    confidence: Mapped[str|None]=mapped_column(String(20),nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow,index=True)
