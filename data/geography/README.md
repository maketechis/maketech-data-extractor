# Geography data

The application imports India geography from a versioned CSV rather than hard-coding administrative divisions in Python.

Required columns:

- state_name
- state_code (optional)
- district_name

The authoritative production dataset should be sourced from India's Local Government Directory (LGD) or another government-published administrative-boundary dataset. Keep the source URL, retrieval date, and dataset version alongside any imported file.

Do not treat district counts as permanently fixed: administrative boundaries and names change over time.
