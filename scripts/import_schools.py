import argparse
from app.database import SessionLocal
from app.services.school_import import import_schools
p=argparse.ArgumentParser(description="Import normalized school base dataset")
p.add_argument("csv")
args=p.parse_args()
with SessionLocal() as db: print(import_schools(db,args.csv))
