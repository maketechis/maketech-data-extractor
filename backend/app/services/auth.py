import hashlib,hmac,secrets
from datetime import datetime,timedelta,timezone
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config import get_settings
from app.models.auth import AppUser
def hash_password(password:str)->str:
    salt=secrets.token_hex(16);digest=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt),310000)
    return "pbkdf2_sha256$310000$"+salt+"$"+digest.hex()
def verify_password(password:str,stored:str)->bool:
    try:
        _,iterations,salt,digest=stored.split("$");candidate=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt),int(iterations)).hex()
        return hmac.compare_digest(candidate,digest)
    except Exception:return False
def authenticate(db:Session,email:str,password:str):
    user=db.scalar(select(AppUser).where(AppUser.email==email.strip().lower(),AppUser.is_active.is_(True)))
    return user if user and verify_password(password,user.password_hash) else None
def token_for(user:AppUser)->str:
    s=get_settings();now=datetime.now(timezone.utc)
    return jwt.encode({"sub":str(user.id),"email":user.email,"admin":user.is_admin,"iat":now,"exp":now+timedelta(hours=12)},s.auth_secret,algorithm="HS256")
