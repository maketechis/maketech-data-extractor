# Siwan live acceptance test

This is the first controlled real-data acceptance test.

Target:
- Entity type: Bookseller
- Country: India
- State: Bihar
- District: Siwan
- Live source: OpenStreetMap

The test is intentionally one district only. It must not be expanded into a nationwide run against public OSM community endpoints.

Expected flow:
1. Apply migrations to the development PostgreSQL database.
2. Seed India / Bihar / Siwan and Bookseller.
3. Run the Siwan bookseller script or collector API.
4. Confirm raw/unique/saved statistics.
5. Inspect saved entities and provenance.
6. Do not interpret the result as an exhaustive registry of all Siwan booksellers.
