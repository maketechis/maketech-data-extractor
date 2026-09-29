# Phase 14 — verified-site contact extraction

Only websites with verification_status verified or likely are eligible for crawling.

The crawler:
- starts from the accepted website URL
- stays on the same hostname
- prioritizes Contact/About/Reach Us/Location pages
- defaults to a maximum of 5 HTML pages
- follows normal HTTP behavior only; it does not bypass authentication, CAPTCHAs, access controls, or anti-bot restrictions

Extraction confidence:
- mailto email: 1.00
- tel phone: 1.00
- visible email regex: 0.85
- visible Indian phone regex: 0.80
- address semantic/DOM element: 0.85
- Indian PIN regex: 0.75

Every extracted phone/email stores the exact source page URL and confidence. Address/PIN are filled only when currently missing. Existing master values are not overwritten.

These confidence values are initial heuristics and must be calibrated against real labeled examples before large-scale automatic acceptance.
