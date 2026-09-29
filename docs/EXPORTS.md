# Phase 17 — Excel and CSV exports

Exports are generated from normalized database records rather than raw source rows.

Excel sheets:
- Entities
- Contacts
- Sources
- Needs Review
- District Progress
- Statistics

Exports can be filtered by district. The generic entity export is the base format; entity-specific columns such as UDISE/board for schools will be added once those attributes are persisted in a structured form.

Source/provenance sheets are retained so exported contact information remains auditable.
