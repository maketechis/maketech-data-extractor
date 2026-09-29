# Source registry

Every collector source is registered with:
- supported entity types
- supported countries
- live/offline behavior
- cost class
- priority
- description

The registry lets campaigns select compatible sources without hard-coding provider names into orchestration.

Current registry:
- Versioned CSV Import: generic dataset ingestion
- OpenStreetMap: controlled live development discovery for School/Bookseller

Adding a source to the registry does not imply completeness or permission for bulk use. Each adapter must document provenance, access terms, quotas and coverage limitations.
