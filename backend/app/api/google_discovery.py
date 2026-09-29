from fastapi import APIRouter,HTTPException,Query
from app.sources.google_direct import build_google_query,search_google
router=APIRouter(prefix="/google-discovery",tags=["google-discovery"])

@router.get("/search")
def search(entity_type:str,district:str,state:str,country:str="India",name:str|None=None,limit:int=Query(10,ge=1,le=10)):
    query=build_google_query(entity_type=entity_type,district=district,state=state,country=country,name=name)
    try: results=search_google(query,limit=limit)
    except Exception as exc: raise HTTPException(502,f"Google discovery unavailable: {type(exc).__name__}") from exc
    return {"query":query,"count":len(results),"results":[{"title":x.title,"url":x.url} for x in results]}
