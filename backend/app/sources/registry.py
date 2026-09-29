from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True,slots=True)
class SourceDefinition:
    slug:str
    name:str
    entity_types:tuple[str,...]
    countries:tuple[str,...]
    live:bool
    cost:str
    priority:int
    description:str

SOURCES={
    "osm":SourceDefinition("osm","OpenStreetMap",("bookseller","school"),("*",),True,"free",50,"Community geographic discovery"),
    "csv":SourceDefinition("csv","Versioned CSV Import",("*",),("*",),False,"free",10,"Official/open/manual dataset imports"),
    "google_direct":SourceDefinition("google_direct","Direct Google Web Search",("*",),("*",),True,"free",70,"MVP supplemental and website discovery"),
}

def compatible_sources(*,entity_type:str,country_iso:str):
    return sorted(
        [x for x in SOURCES.values() if ("*" in x.entity_types or entity_type in x.entity_types) and ("*" in x.countries or country_iso in x.countries)],
        key=lambda x:x.priority,
    )
