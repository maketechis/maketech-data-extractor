from app.database import SessionLocal
from app.services.bootstrap import ensure_development_seed
with SessionLocal() as db:
    print(ensure_development_seed(db))
