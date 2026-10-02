from fastapi import APIRouter,Query
from app.source_discovery.service import discover_sources
from app.sources.search_settings import SearchMode,SearchSettings
router=APIRouter(prefix="/source-discovery",tags=["source-discovery"])
@router.get("")
def discover(entity_type:str="school",district:str="Siwan",state:str="Bihar",country:str="India",google:bool=True,bing:bool=True,yahoo:bool=True,mode:SearchMode=SearchMode.ALL,max_results:int=Query(10,ge=1,le=10)):
    settings=SearchSettings(google=google,bing=bing,yahoo=yahoo,mode=mode,max_results=max_results)
    return discover_sources(entity_type=entity_type,district=district,state=state,country=country,settings=settings)
