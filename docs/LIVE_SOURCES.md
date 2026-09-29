# Live discovery sources

## OpenStreetMap development adapter

The first live adapter uses OpenStreetMap data:

1. Nominatim resolves a district/state/country to an OSM administrative relation.
2. Overpass queries that boundary for supported entity tags.
3. Results are converted to the common RawEntity format and retain the exact OSM feature URL as provenance.

Initial mappings:
- Bookseller -> shop=books
- School -> amenity=school

### Important limitations

OpenStreetMap is community-maintained and is not an exhaustive registry of businesses or schools. Coverage varies by district. It is therefore one discovery source, not a completeness guarantee.

Public Nominatim and Overpass instances are suitable only for controlled development/testing. Respect their usage policies and rate limits. Large district/nationwide campaigns must use an appropriate hosted/self-hosted provider or another permitted data source rather than placing bulk load on public community infrastructure.

CI uses no live network calls.
