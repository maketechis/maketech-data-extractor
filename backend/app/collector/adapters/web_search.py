from app.collector.adapters.base import CollectorAdapter
from app.collector.discovery import build_discovery_queries
from app.collector.types import RawEntity
from app.sources.search_settings import SearchSettings
from app.sources.web_search import search_web
class WebSearchAdapter(CollectorAdapter):
    name="web_search"
    def __init__(self,settings:SearchSettings):self.settings=settings
    def collect(self,*,entity_type,district,state,country):
        rows=[]
        for q in build_discovery_queries(entity_type=entity_type,district=district,state=state,country=country):
            for hit in search_web(q.query,self.settings):
                rows.append(RawEntity(name=hit.title,website=hit.url,source_name=hit.engine,source_url=hit.url,attributes={"query":q.query,"engine":hit.engine}))
        return rows
