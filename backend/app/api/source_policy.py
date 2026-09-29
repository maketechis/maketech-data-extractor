from fastapi import APIRouter,Query
from app.sources.policy import SourcePurpose,build_source_plan
router=APIRouter(prefix="/source-policy",tags=["source-policy"])

@router.get("/plan")
def plan(entity_type:str,country_iso:str,purpose:SourcePurpose,allow_paid:bool=Query(False)):
    return [x.__dict__ for x in build_source_plan(entity_type=entity_type,country_iso=country_iso,purpose=purpose,allow_paid=allow_paid)]
