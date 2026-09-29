# Extraction history

The platform keeps current entity data and an append-only operational history.

ExtractionRun records each collection/enrichment execution with campaign, district, timestamps, counts, status and errors.

ExtractionEvent records material entity changes such as:
- entity discovered
- phone/email added
- website candidate/verification changes
- address/PIN filled
- future merge/dedup decisions

Events retain old/new values, exact source URL and confidence when available.

History must not be overwritten when current entity data changes. This enables auditing, re-verification, debugging and before/after comparisons.
