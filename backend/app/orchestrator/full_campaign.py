import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Campaign,CampaignLocation,CampaignStatus,District,LocationStatus
from app.orchestrator.campaign_loop import campaign_stats
from app.orchestrator.district_pipeline import process_district
from app.orchestrator.history import get_or_start_active_run,sync_run
from app.orchestrator.source_pipeline import run_source_pipeline
from app.services.entity_cleanup import merge_exact_duplicates
from app.services.source_entity_cleanup import cleanup_invalid_source_entities

def _quality(source_result,result,duplicates_merged):
    engines=source_result["discovery"].get("engines",{})
    engine_success=sum(1 for x in engines.values() if x.get("status")=="success")
    extracted=source_result["extraction"]["raw_records"]
    direct=result.get("collection",{}).get("raw",0)
    enrichment=result.get("enrichment",{})
    enriched=enrichment.get("complete",0)+enrichment.get("partial",0)
    score=min(100,(20 if engine_success else 0)+(20 if source_result["discovery"]["sources"] else 0)+(30 if extracted>=10 else 15 if extracted>0 else 0)+(10 if direct>0 else 0)+(20 if enriched>0 else 0))
    status="healthy" if score>=70 else "partial" if score>=40 else "degraded"
    return {"score":score,"status":status,"engine_successes":engine_success,"sources_discovered":source_result["discovery"]["sources"],"source_records":extracted,"direct_records":direct,"enriched_entities":enriched,"duplicates_merged":duplicates_merged,"engines":engines,"source_extraction":source_result["extraction"]}

def run_next_full_district(db:Session,campaign_id:int,*,adapters=None,enrichment_limit=25,max_pages=5):
    campaign=db.get(Campaign,campaign_id)
    if not campaign:raise ValueError("Campaign not found")
    if campaign.status==CampaignStatus.PAUSED:return {"campaign_id":campaign_id,"status":"paused"}
    run=get_or_start_active_run(db,campaign_id)
    location=db.scalar(select(CampaignLocation).where(CampaignLocation.campaign_id==campaign_id,CampaignLocation.status==LocationStatus.PENDING).order_by(CampaignLocation.id).limit(1).with_for_update(skip_locked=True))
    if not location:
        stats=campaign_stats(db,campaign_id)
        if stats["pending"]==0 and stats["running"]==0:
            campaign.status=CampaignStatus.COMPLETED if stats["failed"]==0 else CampaignStatus.FAILED;db.commit()
        sync_run(db,run,campaign.status)
        return {"campaign_id":campaign_id,"campaign_run_id":run.id,"status":"no_pending_districts","stats":stats}
    campaign.status=CampaignStatus.RUNNING;db.commit()
    district=db.get(District,location.district_id)
    invalid_cleanup=cleanup_invalid_source_entities(db,district_name=district.name,state_name=db.get(__import__("app.models.core",fromlist=["State"]).State,district.state_id).name)
    before=merge_exact_duplicates(db)["duplicates_merged"]
    source_result=run_source_pipeline(db,campaign,district)
    result=process_district(db,campaign,location,adapters=adapters,enrichment_limit=enrichment_limit,max_pages=max_pages)
    after=merge_exact_duplicates(db)["duplicates_merged"]
    quality_data=_quality(source_result,result,before+after)
    quality_data["invalid_cleanup"]=invalid_cleanup
    campaign.quality_status=quality_data["status"];campaign.quality_json=json.dumps(quality_data);db.commit()
    stats=campaign_stats(db,campaign_id)
    if stats["pending"]==0 and stats["running"]==0:
        campaign.status=CampaignStatus.COMPLETED if stats["failed"]==0 else CampaignStatus.FAILED;db.commit()
    sync_run(db,run,campaign.status)
    return {"campaign_id":campaign_id,"campaign_run_id":run.id,"campaign_status":campaign.status.value,"source_pipeline":source_result,"quality":quality_data,**result,"campaign_stats":stats}
