# Siwan school benchmark

The benchmark is calculated from persisted master entities after import/discovery/deduplication.

Metrics:
- unique schools
- UDISE coverage
- phone coverage
- email coverage
- website coverage
- verified website coverage
- unresolved entities
- unique entities contributed by each provenance source

Endpoint:
GET /benchmarks/schools?state=Bihar&district=Siwan

This benchmark does not claim real-world completeness by itself. Coverage completeness must be evaluated against the authoritative/base dataset and additional source contribution once production data is loaded.
