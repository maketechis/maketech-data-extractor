from sqlalchemy.orm import Session
from app.enrichment.persist import persist_extracted_values
from app.enrichment.site_crawler import crawl_verified_site
from app.models.core import Entity, EntityWebsite

ALLOWED_STATUSES={"verified","likely"}

def enrich_from_website(db: Session, website: EntityWebsite, max_pages: int=5):
    if website.verification_status not in ALLOWED_STATUSES:
        raise ValueError("Website must be verified or likely before crawling")
    entity=db.get(Entity,website.entity_id)
    pages=crawl_verified_site(website.url,max_pages=max_pages)
    values=[value for page in pages for value in page["values"]]
    result=persist_extracted_values(db,entity,values)
    return {"entity_id":entity.id,"website_id":website.id,"pages_crawled":len(pages),"values_found":len(values),**result}
