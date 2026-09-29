from dataclasses import dataclass
from enum import StrEnum
from app.sources.registry import SourceDefinition,compatible_sources

class SourcePurpose(StrEnum):
    ENTITY_LIST="entity_list"
    SUPPLEMENTAL_DISCOVERY="supplemental_discovery"
    WEBSITE_DISCOVERY="website_discovery"
    CONTACT_ENRICHMENT="contact_enrichment"

@dataclass(frozen=True,slots=True)
class SourcePlanItem:
    slug:str
    purpose:str
    priority:int
    required:bool
    cost:str

PURPOSE_RULES={
    "csv":{SourcePurpose.ENTITY_LIST:10},
    "osm":{SourcePurpose.SUPPLEMENTAL_DISCOVERY:50},
    "google_direct":{SourcePurpose.SUPPLEMENTAL_DISCOVERY:70,SourcePurpose.WEBSITE_DISCOVERY:20},
}

def build_source_plan(*,entity_type:str,country_iso:str,purpose:SourcePurpose,allow_paid:bool=False):
    plan=[]
    for source in compatible_sources(entity_type=entity_type,country_iso=country_iso):
        priority=PURPOSE_RULES.get(source.slug,{}).get(purpose)
        if priority is None: continue
        if source.cost!="free" and not allow_paid: continue
        plan.append(SourcePlanItem(source.slug,purpose.value,priority,False,source.cost))
    return sorted(plan,key=lambda x:x.priority)
