from abc import ABC, abstractmethod
from collections.abc import Iterable
from app.collector.types import RawEntity

class CollectorAdapter(ABC):
    name: str

    @abstractmethod
    def collect(self, *, entity_type: str, district: str, state: str, country: str) -> Iterable[RawEntity]:
        raise NotImplementedError
