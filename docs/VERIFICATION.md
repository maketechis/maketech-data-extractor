# Website identity verification

Search ranking is never treated as identity proof.

Candidate websites are scored from page evidence:
- strong entity-name match
- district
- state/region
- PIN/postal code
- existing phone or email

Initial thresholds:
- 75–100: verified
- 55–74: likely
- 30–54: needs_review
- below 30: rejected

These thresholds are an initial heuristic and must be calibrated against labeled examples before large-scale automatic acceptance.

The verification fetcher performs a normal HTTP request only. It does not bypass authentication, CAPTCHAs, access controls, or anti-bot restrictions.
