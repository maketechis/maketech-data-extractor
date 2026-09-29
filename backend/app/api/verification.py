from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import EntityWebsite
from app.verification.fetcher import fetch_page_text
from app.verification.website_matcher import apply_match, score_candidate

router=APIRouter(prefix="/verification",tags=["verification"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/websites/{website_id}")
def verify_website(website_id:int,db:Session=Depends(get_db)):
    website=db.get(EntityWebsite,website_id)
    if not website: raise HTTPException(404,"Website candidate not found")
    try: text=fetch_page_text(website.url)
    except Exception as exc: raise HTTPException(502,f"Candidate fetch failed: {type(exc).__name__}") from exc
    entity=website.entity_id and db.get(__import__("app.models.core",fromlist=["Entity"]).Entity,website.entity_id)
    result=score_candidate(db,entity,text)
    apply_match(db,website,result)
    return {"website_id":website.id,"score":result.score,"status":result.status,"evidence":result.evidence}
