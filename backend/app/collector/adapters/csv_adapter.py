import csv
from pathlib import Path
from app.collector.adapters.base import CollectorAdapter
from app.collector.types import RawEntity

class CSVAdapter(CollectorAdapter):
    name="csv"

    def __init__(self,path):
        self.path=Path(path)

    def collect(self, *, entity_type, district, state, country):
        with self.path.open(newline="",encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                if row.get("district","").strip().lower()!=district.lower(): continue
                if row.get("state","").strip().lower()!=state.lower(): continue
                yield RawEntity(name=row["name"],address=row.get("address") or None,pin=row.get("pin") or None,phone=row.get("phone") or None,email=row.get("email") or None,website=row.get("website") or None,source_name=row.get("source_name") or self.name,source_url=row.get("source_url") or f"file://{self.path.name}",source_record_id=row.get("source_record_id") or None)
