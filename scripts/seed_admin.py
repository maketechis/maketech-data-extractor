import getpass
from sqlalchemy import select
from app.database import SessionLocal
from app.models.auth import AppUser
from app.services.auth import hash_password
EMAIL="rabbaniindia2000@gmail.com"
password=getpass.getpass("Password for "+EMAIL+": ")
if len(password)<10:raise SystemExit("Password must be at least 10 characters")
with SessionLocal() as db:
    user=db.scalar(select(AppUser).where(AppUser.email==EMAIL))
    if user:user.password_hash=hash_password(password);user.is_active=True;user.is_admin=True
    else:db.add(AppUser(email=EMAIL,password_hash=hash_password(password),is_active=True,is_admin=True))
    db.commit()
print("Admin credential created/updated.")
