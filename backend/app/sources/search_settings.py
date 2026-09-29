from dataclasses import dataclass,field
from enum import StrEnum

class SearchMode(StrEnum):
    FALLBACK="fallback"
    ALL="all"

SUPPORTED_ENGINES=("google","bing","yahoo")

@dataclass(slots=True)
class SearchSettings:
    google:bool=True
    bing:bool=True
    yahoo:bool=True
    mode:SearchMode=SearchMode.FALLBACK
    max_results:int=10

    def enabled_engines(self)->list[str]:
        return [name for name in SUPPORTED_ENGINES if getattr(self,name)]
