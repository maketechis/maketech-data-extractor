from io import BytesIO
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.exporters.csv_export import build_csv
from app.exporters.excel import build_excel

router=APIRouter(prefix="/exports",tags=["exports"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/excel")
def excel(district_id:int|None=Query(None),db:Session=Depends(get_db)):
    data=build_excel(db,district_id=district_id)
    headers={"Content-Disposition":'attachment; filename="data-extractor.xlsx"'}
    return StreamingResponse(BytesIO(data),media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",headers=headers)

@router.get("/csv")
def csv(district_id:int|None=Query(None),db:Session=Depends(get_db)):
    data=build_csv(db,district_id=district_id)
    return Response(data,media_type="text/csv",headers={"Content-Disposition":'attachment; filename="data-extractor.csv"'})
