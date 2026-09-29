import argparse
from app.database import SessionLocal
from app.services.geography_import import import_india_geography

parser=argparse.ArgumentParser()
parser.add_argument("csv")
args=parser.parse_args()
with SessionLocal() as db:
    print(import_india_geography(db,args.csv))
