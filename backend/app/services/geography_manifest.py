import json
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class GeographyManifest:
    country_iso:str
    source_name:str
    source_url:str
    retrieved_at:str
    version:str

def load_manifest(path:str|Path)->GeographyManifest:
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    return GeographyManifest(**data)
