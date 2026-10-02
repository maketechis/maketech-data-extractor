from app.database import SessionLocal
from app.services.bootstrap import bootstrap_core
with SessionLocal() as db:
    print(bootstrap_core(db))
