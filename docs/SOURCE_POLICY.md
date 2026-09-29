# Purpose-aware source policy

Source selection is based on the job being performed, not a single global ranking.

Purposes:
- entity_list: establish the base registry/list
- supplemental_discovery: find additional candidates
- website_discovery: find candidate official websites
- contact_enrichment: fill missing contact fields from accepted sources

Policy inputs:
entity type, country, purpose, enabled sources, cost permission.

Paid sources are excluded unless explicitly allowed. A source may participate in one purpose but not another.

Initial rules:
- versioned CSV/imported datasets -> entity_list
- OpenStreetMap -> supplemental_discovery

As real school/search providers are added, they register their supported purposes and priorities here. The orchestrator should execute a plan rather than hard-code provider names.

Source failure semantics:
- optional source failure is recorded and processing continues
- a future required=true source can block the stage
- source provenance remains attached to every collected record
