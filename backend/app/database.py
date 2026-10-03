from sqlalchemy import create_engine,event
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from app.config import get_settings
settings=get_settings()
kwargs={"pool_pre_ping":True}
if settings.database_url.startswith("sqlite:"):kwargs["connect_args"]={"check_same_thread":False}
engine=create_engine(settings.database_url,**kwargs)
if settings.database_url.startswith("sqlite:"):
    @event.listens_for(engine,"connect")
    def _sqlite_pragmas(conn,_):
        cur=conn.cursor();cur.execute("PRAGMA foreign_keys=ON");cur.execute("PRAGMA journal_mode=WAL");cur.close()
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
class Base(DeclarativeBase):pass
