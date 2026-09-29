# India geography validation

Run after importing production LGD state and district files:

PYTHONPATH=backend python scripts/validate_india_geography.py

Hard failures:
- India missing
- no states/districts
- missing LGD codes
- duplicate LGD codes
- duplicate normalized district within a state
- Bihar or Siwan missing

Warnings flag suspiciously small imports. Thresholds are sanity checks, not official permanent counts, because administrative geography changes over time.

The production source manifest remains the authority for source/version/date.
