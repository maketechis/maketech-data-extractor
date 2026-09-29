# Direct Google discovery — MVP

The MVP can issue ordinary Google web-search requests directly, with no paid API.

Use cases:
- supplemental entity discovery, especially businesses
- candidate official-website discovery for known entities

Rules:
- maximum 10 results per request
- no CAPTCHA solving or anti-bot bypass
- if Google blocks/limits access, record the source as unavailable and stop that request
- exact destination URLs remain provenance when later used
- Google search ranking is never treated as verification
- candidate websites must still pass the existing identity-verification gate before contact crawling
- no paid API/proxy fallback is enabled

This adapter is intentionally isolated so it can be replaced later if direct result-page access proves unreliable.
