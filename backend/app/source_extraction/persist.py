from sqlalchemy.orm import Session
from app.collector.engine import CollectorEngine
from app.collector.types import RawEntity
class ExtractedAdapter:
    name="extracted_source"
    def __init__(self,records):self.records=records
    def collect(self,**kwargs):
        return [RawEntity(name=x["name"],address=x.get("address"),pin=x.get("pin"),phone=x.get("phone"),email=x.get("email"),website=x.get("website"),source_name="source_extraction",source_url=x["source_url"],source_record_id=x.get("source_record_id"),attributes={"extracted":True}) for x in self.records]
def persist_extracted(db:Session,records,*,entity_type,country,state,district):
    return CollectorEngine([ExtractedAdapter(records)]).collect(db=db,entity_type=entity_type,country=country,state=state,district=district)
