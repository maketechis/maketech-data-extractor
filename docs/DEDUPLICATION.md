# Phase 19 — Cross-source deduplication

Incoming records are matched only against entities of the same type and district.

Initial evidence weights:
- near-exact normalized name: 45
- similar normalized name: 30
- same PIN: 20
- same normalized phone: 40
- same website domain: 40

Decision thresholds:
- 70+: merge
- 50–69: review
- below 50: treat as new

Automatic merge fills missing master fields and appends new contacts, websites and source provenance. Existing populated address/PIN values are not overwritten.

These are initial heuristics. Before nationwide use they must be calibrated on labeled duplicate/non-duplicate examples. Ambiguous matches must remain reviewable rather than being destructively merged.
