from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Campaign,CampaignSource,Country,District,EntityType,State
from app.source_extraction.service import extract_source
from app.source_extraction.persist import persist_extracted
from app.source_extraction.validation import filter_records
from app.sources.google_direct import search_google_pages
def query_for(et,district,state,country):return f"{et} list of {district}"
def discover_and_store(db:Session,campaign:Campaign,district:District,pages:int=5):
    et=db.get(EntityType,campaign.entity_type_id);state=db.get(State,district.state_id);country=db.get(Country,campaign.country_id);q=query_for(et.slug,district.name,state.name,country.name)
    existing=db.scalars(select(CampaignSource).where(CampaignSource.campaign_id==campaign.id,CampaignSource.district_id==district.id)).all()
    completed_pages={x.page_number for x in existing}
    if len(completed_pages)>=pages:return {"query":q,"pages":pages,"results":len(existing),"sources_saved":0,"page_diagnostics":[{"page":p,"status":"cached","results":sum(1 for x in existing if x.page_number==p),"error":None} for p in range(1,pages+1)],"status":"cached"}
    hits,diagnostics=search_google_pages(q,pages=pages,delay_seconds=20);created=0
    for hit in hits:
        if db.scalar(select(CampaignSource.id).where(CampaignSource.campaign_id==campaign.id,CampaignSource.url==hit.url)):continue
        db.add(CampaignSource(campaign_id=campaign.id,district_id=district.id,engine="google",query=q,page_number=hit.page,rank=hit.rank,title=hit.title,url=hit.url));created+=1
    db.commit();return {"query":q,"pages":pages,"results":len(hits),"sources_saved":created,"page_diagnostics":diagnostics,"status":"success" if hits else "degraded"}
def extract_saved_sources(db:Session,campaign:Campaign,district:District):
    et=db.get(EntityType,campaign.entity_type_id);state=db.get(State,district.state_id);country=db.get(Country,campaign.country_id)
    rows=db.scalars(select(CampaignSource).where(CampaignSource.campaign_id==campaign.id,CampaignSource.district_id==district.id).order_by(CampaignSource.page_number,CampaignSource.rank)).all()
    raw=accepted=saved=failed=0
    for src in rows:
        if src.status=="completed":raw+=src.records_raw;accepted+=src.records_accepted;saved+=src.records_saved;continue
        src.status="extracting";db.commit()
        try:
            data=extract_source(src.url,district=district.name);valid,stats=filter_records(data["records"],district=district.name,state=state.name);src.records_raw=data["count"];src.records_accepted=len(valid);raw+=data["count"];accepted+=len(valid)
            if valid:
                result=persist_extracted(db,valid,entity_type=et,country=country,state=state,district=district);src.records_saved=result["saved"];saved+=result["saved"]
            src.status="completed";src.last_error=None;db.commit()
        except Exception as exc:
            db.rollback();src=db.get(CampaignSource,src.id);src.status="failed";src.last_error=f"{type(exc).__name__}: {str(exc)[:500]}";db.commit();failed+=1
    return {"sources":len(rows),"raw":raw,"accepted":accepted,"saved":saved,"failed_sources":failed}
def run_simple_source_pipeline(db,campaign,district):
    discovery=discover_and_store(db,campaign,district,5);extraction=extract_saved_sources(db,campaign,district);return {"discovery":discovery,"extraction":extraction}
