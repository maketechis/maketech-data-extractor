from fastapi import APIRouter
from app.sources.registry import SOURCES,compatible_sources

router=APIRouter(prefix="/sources",tags=["sources"])

@router.get("")
def list_sources():
    return [x.__dict__ for x in SOURCES.values()]

@router.get("/compatible")
def compatible(entity_type:str,country_iso:str):
    return [x.__dict__ for x in compatible_sources(entity_type=entity_type,country_iso=country_iso)]
