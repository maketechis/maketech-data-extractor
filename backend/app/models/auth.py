from datetime import datetime,timezone
from sqlalchemy import Boolean,DateTime,String
from sqlalchemy.orm import Mapped,mapped_column
from app.database import Base
def utcnow(): return datetime.now(timezone.utc)
class AppUser(Base):
    __tablename__="app_users"
    id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]=mapped_column(String(320),unique=True,index=True)
    password_hash:Mapped[str]=mapped_column(String(255))
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    is_admin:Mapped[bool]=mapped_column(Boolean,default=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
