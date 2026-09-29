# District orchestration

A campaign queue is persisted in campaign_locations. The runner claims one pending district, marks it running, executes System 1, stores run counts, and marks the district completed or failed.

A failed district does not imply the campaign must stop. A later worker/scheduler phase will implement retry policy and automatic continuation.

Current live default adapter is OpenStreetMap and is restricted to controlled development testing. Do not use the public OSM endpoints for a nationwide campaign.
