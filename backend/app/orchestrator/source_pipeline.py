from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Campaign,Country,District,EntityType,State
from app.source_discovery.service import discover_sources
from app.source_extraction.service import extract_source
from app.source_extraction.persist import persist_extracted
from app.sources.search_settings import SearchMode,SearchSettings
def run_source_pipeline(db:Session,campaign:Campaign,district:District,max_sources:int=8)->dict:
    state=db.get(State,district.state_id);country=db.get(Country,campaign.country_id);et=db.get(EntityType,campaign.entity_type_id)
    settings=SearchSettings(google=campaign.search_google,bing=campaign.search_bing,yahoo=campaign.search_yahoo,mode=SearchMode.ALL,max_results=10)
    discovered=discover_sources(entity_type=et.slug,district=district.name,state=state.name,country=country.name,settings=settings)
    extracted=saved=merged=0;source_runs=[]
    for src in discovered["sources"][:max_sources]:
        if src["score"]<20:continue
        try:
            data=extract_source(src["url"])
            if not data["records"]:source_runs.append({"url":src["url"],"status":"empty","records":0});continue
            result=persist_extracted(db,data["records"],entity_type=et,country=country,state=state,district=district)
            extracted+=data["count"];saved+=result["saved"];merged+=result["merged"];source_runs.append({"url":src["url"],"status":"extracted","records":data["count"],"saved":result["saved"],"merged":result["merged"]})
        except Exception as exc:source_runs.append({"url":src["url"],"status":"failed","error":type(exc).__name__})
    return {"discovery":{"queries":discovered["queries"],"metrics":discovered["metrics"],"sources":len(discovered["sources"])},"extraction":{"sources_attempted":len(source_runs),"raw_records":extracted,"saved":saved,"merged":merged,"runs":source_runs}}
