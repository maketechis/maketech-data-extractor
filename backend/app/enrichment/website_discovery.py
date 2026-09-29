from abc import ABC, abstractmethod
from collections.abc import Iterable
from sqlalchemy.orm import Session
from app.enrichment.candidates import WebsiteCandidate, candidate_query, store_candidate
from app.models.core import Entity

class WebsiteDiscoveryProvider(ABC):
    @abstractmethod
    def search(self, query: str) -> Iterable[WebsiteCandidate]:
        raise NotImplementedError

class FixtureWebsiteDiscovery(WebsiteDiscoveryProvider):
    def __init__(self,results): self.results=results
    def search(self,query): yield from self.results.get(query,[])

def discover_candidates(db: Session, entity: Entity, provider: WebsiteDiscoveryProvider, limit: int=5):
    query=candidate_query(db,entity); stored=[]
    for candidate in list(provider.search(query))[:limit]:
        stored.append(store_candidate(db,entity,candidate))
    return {"entity_id":entity.id,"query":query,"candidates":[{"id":x.id,"url":x.url,"domain":x.domain,"status":x.verification_status} for x in stored]}
