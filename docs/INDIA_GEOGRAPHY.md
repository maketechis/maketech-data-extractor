# India production geography

The importer already supports Country -> State/UT -> District.

Production data must be loaded from a dated/versioned authoritative government administrative dataset. The repository stores a manifest containing source name, source URL, retrieval date and version alongside the normalized CSV.

We deliberately do not hard-code a permanent district count: administrative districts and names can change.

Required normalized CSV columns:
state_name,state_code,district_name

Acceptance checks before import:
- country ISO = IN
- no blank state/district names
- no duplicate state + district pairs
- source manifest is complete
- Bihar / Siwan exists
