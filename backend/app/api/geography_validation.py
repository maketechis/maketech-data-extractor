from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.geography_validation import validate_india_geography
router=APIRouter(prefix="/geography-validation",tags=["geography-validation"])
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
@router.get("/india")
def india(db:Session=Depends(get_db)):
    return validate_india_geography(db)
