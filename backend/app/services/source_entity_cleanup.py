from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Entity,EntityContact,EntitySource,EntityWebsite
from app.source_extraction.validation import validate_record
def cleanup_invalid_source_entities(db:Session,*,district_name:str,state_name:str)->dict:
    ids=db.scalars(select(EntitySource.entity_id).where(EntitySource.source_type=="source_extraction").distinct()).all()
    removed=websites_removed=0
    for entity_id in ids:
        e=db.get(Entity,entity_id)
        if not e:continue
        sites=db.scalars(select(EntityWebsite).where(EntityWebsite.entity_id==e.id)).all()
        website=sites[0].url if sites else None
        row={"name":e.name,"address":e.address,"website":website}
        ok,_=validate_record(row,district=district_name,state=state_name)
        for site in sites:
            if any(x in site.domain.casefold() for x in ("google.com","google.co.","bing.com","yahoo.com")):
                db.delete(site);websites_removed+=1
        if ok:continue
        for x in db.scalars(select(EntityContact).where(EntityContact.entity_id==e.id)).all():db.delete(x)
        for x in db.scalars(select(EntityWebsite).where(EntityWebsite.entity_id==e.id)).all():db.delete(x)
        for x in db.scalars(select(EntitySource).where(EntitySource.entity_id==e.id)).all():db.delete(x)
        db.delete(e);removed+=1
    db.commit();return {"invalid_entities_removed":removed,"search_websites_removed":websites_removed}
