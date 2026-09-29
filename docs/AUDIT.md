# Pre-source-expansion audit

Before adding more live sources, the backend was reviewed for integration gaps.

Fixed:
- environment file resolution no longer depends on current working directory
- runtime safety settings are represented in typed configuration
- health endpoint reflects implemented enrichment/history/export systems
- district enrichment is scoped to the campaign entity type, preventing a Bookseller campaign from enriching School records in the same district
- district saved counts include records merged into existing master entities
- pipeline exception handling rolls back the failed transaction before recording FAILED status
- campaign-history helper added for active-run snapshot/finalization integration

Remaining deliberate work:
- campaign history must be wired into every campaign execution endpoint
- production worker/lease model for concurrent campaigns
- generic international administrative-level model
- structured entity-specific attributes such as UDISE/board/block
- real India geography dataset and additional permitted source adapters
- stronger SSRF/URL safety before arbitrary discovered websites are crawled
