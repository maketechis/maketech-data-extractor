from app.database import SessionLocal
from app.services.geography_validation import validate_india_geography
with SessionLocal() as db:
    result=validate_india_geography(db)
    print(result)
    raise SystemExit(0 if result["valid"] else 1)
