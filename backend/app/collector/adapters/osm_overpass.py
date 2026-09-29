import re
import httpx
from app.collector.adapters.base import CollectorAdapter
from app.collector.types import RawEntity

class OSMOverpassAdapter(CollectorAdapter):
    """Low-volume OpenStreetMap discovery adapter for development.

    Uses Nominatim to resolve the district boundary and Overpass to retrieve
    matching OSM features. Endpoints are configurable so production is not
    coupled to a public community instance.
    """
    name="openstreetmap"

    def __init__(self, *, timeout=30.0,
                 nominatim_url="https://nominatim.openstreetmap.org/search",
                 overpass_url="https://overpass-api.de/api/interpreter",
                 user_agent="MakeTechDataExtractor/0.1 (development)"):
        self.timeout=timeout
        self.nominatim_url=nominatim_url
        self.overpass_url=overpass_url
        self.headers={"User-Agent":user_agent}

    def _area_id(self, district, state, country):
        params={"q":f"{district}, {state}, {country}","format":"jsonv2","limit":5,"addressdetails":1}
        with httpx.Client(timeout=self.timeout,headers=self.headers) as client:
            rows=client.get(self.nominatim_url,params=params).raise_for_status().json()
        for row in rows:
            if row.get("osm_type")=="relation":
                return 3600000000 + int(row["osm_id"])
        raise LookupError(f"No OSM relation found for {district}, {state}, {country}")

    def _query(self, area_id, entity_type):
        if entity_type=="bookseller":
            selectors=['nwr["shop"="books"](area.searchArea);']
        elif entity_type=="school":
            selectors=['nwr["amenity"="school"](area.searchArea);']
        else:
            raise ValueError(f"OSM adapter does not support entity type: {entity_type}")
        return f'[out:json][timeout:25];area({area_id})->.searchArea;('+"".join(selectors)+');out center tags;'

    def collect(self, *, entity_type, district, state, country):
        area_id=self._area_id(district,state,country)
        query=self._query(area_id,entity_type)
        with httpx.Client(timeout=self.timeout,headers=self.headers) as client:
            payload=client.post(self.overpass_url,data={"data":query}).raise_for_status().json()
        for item in payload.get("elements",[]):
            tags=item.get("tags",{})
            name=tags.get("name") or tags.get("name:en")
            if not name: continue
            phone=tags.get("contact:phone") or tags.get("phone")
            email=tags.get("contact:email") or tags.get("email")
            website=tags.get("contact:website") or tags.get("website")
            address=", ".join(x for x in [
                tags.get("addr:housenumber"),tags.get("addr:street"),tags.get("addr:city")
            ] if x) or None
            yield RawEntity(
                name=name,address=address,pin=tags.get("addr:postcode"),phone=phone,email=email,website=website,
                source_name=self.name,
                source_url=f"https://www.openstreetmap.org/{item['type']}/{item['id']}",
                source_record_id=f"osm:{item['type']}:{item['id']}",
                attributes={"osm_tags":tags},
            )
