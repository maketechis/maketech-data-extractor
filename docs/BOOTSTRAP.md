# Core bootstrap

Run after migrations:
PYTHONPATH=backend python scripts/bootstrap_core.py

Creates idempotently: India (IN), School, Bookseller.

State/district geography is not hard-coded. Load it through the LGD importer:
PYTHONPATH=backend python scripts/import_lgd.py --states states.csv --districts districts.csv
PYTHONPATH=backend python scripts/validate_india_geography.py
