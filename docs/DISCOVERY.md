# Discovery providers

System 1 separates query generation from search providers.

For a campaign such as `Bookseller / India / district-wise`, the orchestrator supplies the district and the discovery layer generates entity-specific queries. Provider adapters convert search results into `RawEntity` records with source provenance.

## Provider rules

- No paid provider is enabled by default.
- CI never calls live search providers.
- Provider credentials belong in environment variables/secrets.
- Respect provider terms, quotas, robots/access restrictions, and applicable law.
- A district marked complete means configured discovery strategies finished; it does not claim every real-world entity was found.
- New providers must implement `SearchDiscoveryAdapter.search()`.

The first production provider will be selected separately so the core collector is not coupled to Google, Bing, or any directory.
