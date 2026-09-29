# Phase 15 — Enrichment job engine

The job engine composes the deterministic System 2 components that are safe to run automatically after a website has already passed identity verification.

Entity outcomes:
- complete: no missing target fields remain
- partial: an accepted website was crawled but some target fields remain missing
- needs_discovery: no website/candidate exists yet
- needs_review: candidate websites exist but none is accepted

Important boundary: this phase does not automatically turn search candidates into verified websites. Candidate discovery and identity verification remain separate gates.

District enrichment is bounded by entity and page limits. Defaults are intentionally small during development.
