from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.entity_cleanup import merge_exact_duplicates
router=APIRouter(prefix="/maintenance",tags=["maintenance"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
@router.post("/deduplicate-exact")
def deduplicate(db:Session=Depends(get_db)):return merge_exact_duplicates(db)
