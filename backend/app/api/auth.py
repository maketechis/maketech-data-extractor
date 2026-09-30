from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,EmailStr
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.auth import authenticate,token_for
router=APIRouter(prefix="/auth",tags=["auth"])
class Login(BaseModel): email:EmailStr;password:str
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
@router.post("/login")
def login(payload:Login,db:Session=Depends(get_db)):
    user=authenticate(db,payload.email,payload.password)
    if not user:raise HTTPException(401,"Invalid email or password")
    return {"access_token":token_for(user),"token_type":"bearer","user":{"id":user.id,"email":user.email,"is_admin":user.is_admin}}
