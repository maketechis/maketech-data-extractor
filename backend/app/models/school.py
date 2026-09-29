from sqlalchemy import ForeignKey,String,Text,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from app.database import Base

class SchoolProfile(Base):
    __tablename__="school_profiles"
    __table_args__=(UniqueConstraint("udise_code",name="uq_school_profiles_udise_code"),)
    id:Mapped[int]=mapped_column(primary_key=True)
    entity_id:Mapped[int]=mapped_column(ForeignKey("entities.id",ondelete="CASCADE"),unique=True,index=True)
    udise_code:Mapped[str|None]=mapped_column(String(20),nullable=True,index=True)
    block:Mapped[str|None]=mapped_column(String(160),nullable=True,index=True)
    village_town:Mapped[str|None]=mapped_column(String(200),nullable=True)
    management:Mapped[str|None]=mapped_column(String(160),nullable=True)
    category:Mapped[str|None]=mapped_column(String(160),nullable=True)
    board:Mapped[str|None]=mapped_column(String(120),nullable=True)
    attributes_json:Mapped[str|None]=mapped_column(Text,nullable=True)
