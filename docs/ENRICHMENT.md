# System 2 — Information enrichment

System 2 starts by determining what is actually missing. It does not rediscover or overwrite verified values unnecessarily.

Initial enrichment fields:
- phone
- email
- website
- address
- PIN/postal code

The planner produces needs only. It does not yet search the web or modify records.

Next stages:
1. Candidate website discovery.
2. Entity-to-website matching.
3. Controlled page crawling.
4. Deterministic extraction.
5. Provenance and confidence.
6. Human review for ambiguous matches.

This separation is intentional: discovery must not contaminate the master database with an unrelated website.
