from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

def utcnow(): return datetime.now(timezone.utc)

class CampaignRun(Base):
    __tablename__="campaign_runs"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id",ondelete="CASCADE"),index=True)
    status: Mapped[str]=mapped_column(String(30),index=True,default="running")
    started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow,index=True)
    completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    districts_total: Mapped[int]=mapped_column(Integer,default=0)
    districts_completed: Mapped[int]=mapped_column(Integer,default=0)
    districts_failed: Mapped[int]=mapped_column(Integer,default=0)
    records_found: Mapped[int]=mapped_column(Integer,default=0)
    records_saved: Mapped[int]=mapped_column(Integer,default=0)
    notes: Mapped[str|None]=mapped_column(Text,nullable=True)

class CampaignRunDistrict(Base):
    __tablename__="campaign_run_districts"
    id: Mapped[int]=mapped_column(primary_key=True)
    campaign_run_id: Mapped[int]=mapped_column(ForeignKey("campaign_runs.id",ondelete="CASCADE"),index=True)
    district_id: Mapped[int]=mapped_column(ForeignKey("districts.id",ondelete="RESTRICT"),index=True)
    status: Mapped[str]=mapped_column(String(30),index=True)
    attempts: Mapped[int]=mapped_column(Integer,default=0)
    records_found: Mapped[int]=mapped_column(Integer,default=0)
    records_saved: Mapped[int]=mapped_column(Integer,default=0)
    started_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    last_error: Mapped[str|None]=mapped_column(Text,nullable=True)
