from fastapi import APIRouter,Depends,UploadFile,File,HTTPException
from pathlib import Path
from tempfile import NamedTemporaryFile
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import District,Entity,EntityType,State
from app.models.school import SchoolProfile
from app.services.school_import import import_schools
router=APIRouter(prefix="/school-data",tags=["school-data"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
@router.get("/coverage")
def coverage(state:str="Bihar",district:str="Siwan",db:Session=Depends(get_db)):
    et=db.scalar(select(EntityType).where(EntityType.slug=="school"));s=db.scalar(select(State).where(State.name==state))
    d=db.scalar(select(District).where(District.state_id==s.id,District.name==district)) if s else None
    if not et or not d:raise HTTPException(404,"School type or geography not found")
    total=db.scalar(select(func.count(Entity.id)).where(Entity.entity_type_id==et.id,Entity.district_id==d.id)) or 0
    udise=db.scalar(select(func.count(SchoolProfile.id)).join(Entity,Entity.id==SchoolProfile.entity_id).where(Entity.district_id==d.id,SchoolProfile.udise_code.is_not(None))) or 0
    return {"state":state,"district":district,"schools":total,"with_udise":udise,"without_udise":total-udise}
@router.post("/import")
async def upload(file:UploadFile=File(...),db:Session=Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith(".csv"):raise HTTPException(400,"CSV file required")
    with NamedTemporaryFile(suffix=".csv",delete=False) as tmp:
        tmp.write(await file.read());path=Path(tmp.name)
    try:return import_schools(db,path)
    finally:path.unlink(missing_ok=True)
