import enum
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

def utcnow(): return datetime.now(timezone.utc)

class CampaignStatus(str, enum.Enum):
    DRAFT="draft"; QUEUED="queued"; RUNNING="running"; PAUSED="paused"; COMPLETED="completed"; FAILED="failed"; CANCELLED="cancelled"
class LocationStatus(str, enum.Enum):
    PENDING="pending"; RUNNING="running"; COLLECTING="collecting"; ENRICHING="enriching"; REVIEW="review"; COMPLETED="completed"; FAILED="failed"

class Country(Base):
    __tablename__="countries"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(120), unique=True, index=True)
    iso_code: Mapped[str]=mapped_column(String(2), unique=True)
class State(Base):
    __tablename__="states"; __table_args__=(UniqueConstraint("country_id","name"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    country_id: Mapped[int]=mapped_column(ForeignKey("countries.id", ondelete="CASCADE"), index=True)
    name: Mapped[str]=mapped_column(String(120), index=True)
    code: Mapped[str|None]=mapped_column(String(20), nullable=True)
class District(Base):
    __tablename__="districts"; __table_args__=(UniqueConstraint("state_id","name"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    state_id: Mapped[int]=mapped_column(ForeignKey("states.id", ondelete="CASCADE"), index=True)
    name: Mapped[str]=mapped_column(String(160), index=True)
    normalized_name: Mapped[str]=mapped_column(String(160), index=True)
class EntityType(Base):
    __tablename__="entity_types"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(120), unique=True)
    slug: Mapped[str]=mapped_column(String(120), unique=True, index=True)
    config_json: Mapped[str|None]=mapped_column(Text, nullable=True)
class Entity(Base):
    __tablename__="entities"
    id: Mapped[int]=mapped_column(primary_key=True)
    entity_type_id: Mapped[int]=mapped_column(ForeignKey("entity_types.id"), index=True)
    name: Mapped[str]=mapped_column(String(300), index=True)
    normalized_name: Mapped[str]=mapped_column(String(300), index=True)
    country_id: Mapped[int]=mapped_column(ForeignKey("countries.id"), index=True)
    state_id: Mapped[int|None]=mapped_column(ForeignKey("states.id"), nullable=True, index=True)
    district_id: Mapped[int|None]=mapped_column(ForeignKey("districts.id"), nullable=True, index=True)
    address: Mapped[str|None]=mapped_column(Text, nullable=True)
    pin: Mapped[str|None]=mapped_column(String(20), nullable=True, index=True)
    latitude: Mapped[float|None]=mapped_column(Float, nullable=True)
    longitude: Mapped[float|None]=mapped_column(Float, nullable=True)
    status: Mapped[str]=mapped_column(String(40), default="active")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
class EntityContact(Base):
    __tablename__="entity_contacts"
    id: Mapped[int]=mapped_column(primary_key=True)
    entity_id: Mapped[int]=mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), index=True)
    contact_type: Mapped[str]=mapped_column(String(30), index=True)
    value: Mapped[str]=mapped_column(String(500)); source_url: Mapped[str|None]=mapped_column(Text, nullable=True)
    confidence: Mapped[float|None]=mapped_column(Float, nullable=True); verified: Mapped[bool]=mapped_column(Boolean, default=False)
class EntityWebsite(Base):
    __tablename__="entity_websites"
    id: Mapped[int]=mapped_column(primary_key=True)
    entity_id: Mapped[int]=mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), index=True)
    url: Mapped[str]=mapped_column(Text); domain: Mapped[str]=mapped_column(String(255), index=True)
    confidence: Mapped[float|None]=mapped_column(Float, nullable=True); verification_status: Mapped[str]=mapped_column(String(40), default="unverified")
class EntitySource(Base):
    __tablename__="entity_sources"
    id: Mapped[int]=mapped_column(primary_key=True)
    entity_id: Mapped[int]=mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), index=True)
    source_type: Mapped[str]=mapped_column(String(80), index=True); source_url: Mapped[str]=mapped_column(Text)
    source_record_id: Mapped[str|None]=mapped_column(String(255), nullable=True); collected_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
class Campaign(Base):
    __tablename__="campaigns"
    id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(200))
    entity_type_id: Mapped[int]=mapped_column(ForeignKey("entity_types.id"), index=True); country_id: Mapped[int]=mapped_column(ForeignKey("countries.id"), index=True)
    collection_level: Mapped[str]=mapped_column(String(30), default="district"); status: Mapped[CampaignStatus]=mapped_column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
class CampaignLocation(Base):
    __tablename__="campaign_locations"; __table_args__=(UniqueConstraint("campaign_id","district_id"),)
    id: Mapped[int]=mapped_column(primary_key=True); campaign_id: Mapped[int]=mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"), index=True)
    state_id: Mapped[int]=mapped_column(ForeignKey("states.id"), index=True); district_id: Mapped[int]=mapped_column(ForeignKey("districts.id"), index=True)
    status: Mapped[LocationStatus]=mapped_column(Enum(LocationStatus), default=LocationStatus.PENDING, index=True); attempts: Mapped[int]=mapped_column(Integer, default=0)
    records_found: Mapped[int]=mapped_column(Integer, default=0); records_saved: Mapped[int]=mapped_column(Integer, default=0)
    last_error: Mapped[str|None]=mapped_column(Text, nullable=True); started_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True), nullable=True); completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True), nullable=True)
