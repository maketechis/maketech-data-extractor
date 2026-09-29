from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.benchmarks.school import school_benchmark
from app.database import SessionLocal
router=APIRouter(prefix="/benchmarks",tags=["benchmarks"])
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
@router.get("/schools")
def schools(state:str="Bihar",district:str="Siwan",db:Session=Depends(get_db)):
    try: return school_benchmark(db,state_name=state,district_name=district)
    except ValueError as exc: raise HTTPException(404,str(exc)) from exc
