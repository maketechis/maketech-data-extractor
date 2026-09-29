# District completion rules

A district is marked COMPLETED when the configured processing workflow has finished, not when every possible entity has perfect contact data.

Required processing stages:
1. Configured System 1 collection attempted successfully.
2. Raw results normalized/deduplicated/persisted.
3. System 2 enrichment attempted for the bounded entity set.
4. Unresolved outcomes are counted and retained.

Unresolved entity outcomes may include partial, needs_discovery, or needs_review. These do not block geographic progression.

A district is FAILED only when a pipeline stage itself fails. This distinction prevents one business with no public email/website from blocking an India-wide campaign forever.

COMPLETED does not claim exhaustive real-world coverage. It means the configured collection/enrichment workflow completed.
