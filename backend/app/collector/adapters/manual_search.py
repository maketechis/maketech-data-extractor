from collections.abc import Iterable
from app.collector.adapters.search_base import SearchDiscoveryAdapter
from app.collector.types import RawEntity

class FixtureSearchAdapter(SearchDiscoveryAdapter):
    """Deterministic development adapter.

    Live providers plug into SearchDiscoveryAdapter later. CI never calls a real
    search engine, preventing accidental paid requests or brittle network tests.
    """
    name="fixture-search"

    def __init__(self, results_by_query: dict[str,list[RawEntity]]):
        self.results_by_query=results_by_query

    def search(self, query: str) -> Iterable[RawEntity]:
        yield from self.results_by_query.get(query,[])
