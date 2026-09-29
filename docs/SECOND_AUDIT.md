# Second audit

Security:
- arbitrary website fetches must pass public HTTP(S) destination validation
- local and non-public network destinations are rejected

Campaign state:
- the full district pipeline is the canonical System 1 + System 2 execution path
- campaign history is synchronized by the full pipeline

Migrations:
- PostgreSQL CI validates upgrade, downgrade and re-upgrade
- the 0002 migration filename is legacy-named, but its revision is campaign history; the filename is left unchanged to avoid rewriting migration history

Deferred:
- distributed worker leases and heartbeats
- generic international administrative levels
- structured source-specific attributes
- production authentication and authorization
