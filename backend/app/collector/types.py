from dataclasses import dataclass, field

@dataclass(slots=True)
class RawEntity:
    name: str
    source_name: str
    source_url: str
    address: str | None = None
    pin: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    source_record_id: str | None = None
    attributes: dict = field(default_factory=dict)
