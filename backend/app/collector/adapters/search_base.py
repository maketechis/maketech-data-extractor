from abc import abstractmethod
from collections.abc import Iterable
from app.collector.adapters.base import CollectorAdapter
from app.collector.discovery import build_discovery_queries
from app.collector.types import RawEntity

class SearchDiscoveryAdapter(CollectorAdapter):
    synonyms: list[str] | None=None

    @abstractmethod
    def search(self, query: str) -> Iterable[RawEntity]:
        raise NotImplementedError

    def collect(self, *, entity_type, district, state, country):
        for task in build_discovery_queries(entity_type=entity_type,district=district,state=state,country=country,synonyms=self.synonyms):
            yield from self.search(task.query)
