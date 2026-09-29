# LGD production geography

Production India geography uses Government of India Local Government Directory identifiers.

Import order:
1. States/UTs
2. Districts

The importer accepts common LGD CSV header variants and upserts by LGD code first, then by existing geography name. It never deletes missing geography automatically because administrative changes require review.

Example:
PYTHONPATH=backend python scripts/import_lgd.py --states states.csv --districts districts.csv

Keep the source manifest beside the downloaded files with source URL, retrieval date and version/month.
