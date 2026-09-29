from fastapi import APIRouter,Query
from app.sources.search_settings import SearchMode,SearchSettings
from app.sources.web_search import search_web

router=APIRouter(prefix="/web-search",tags=["web-search"])

@router.get("/search")
def search(query:str,google:bool=True,bing:bool=True,yahoo:bool=True,mode:SearchMode=SearchMode.FALLBACK,max_results:int=Query(10,ge=1,le=10)):
    settings=SearchSettings(google=google,bing=bing,yahoo=yahoo,mode=mode,max_results=max_results)
    return {"settings":{"google":google,"bing":bing,"yahoo":yahoo,"mode":mode.value},"results":[x.__dict__ for x in search_web(query,settings)]}
