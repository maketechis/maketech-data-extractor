# Website candidate discovery

Website discovery is separated from verification.

A search provider may propose candidate URLs, but discovery alone never marks a website official or verified. Candidate records start with:
- verification_status = candidate
- confidence = 0

The query uses entity name plus available district, state and PIN.

Next phase scores candidates using evidence from the candidate website and the entity record. Only sufficiently supported matches can become verified; ambiguous candidates go to review.

Live search providers remain disabled by default to avoid accidental paid usage. Provider credentials, if introduced, must be stored as secrets.
