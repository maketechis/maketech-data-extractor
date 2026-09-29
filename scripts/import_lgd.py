import argparse
from app.database import SessionLocal
from app.services.lgd_import import import_lgd_districts,import_lgd_states
p=argparse.ArgumentParser(); p.add_argument("--states",required=True); p.add_argument("--districts",required=True); args=p.parse_args()
with SessionLocal() as db:
    print("states",import_lgd_states(db,args.states))
    print("districts",import_lgd_districts(db,args.districts))
