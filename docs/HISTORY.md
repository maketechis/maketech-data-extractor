# Campaign history

Campaign history preserves each execution of a campaign so previous runs remain visible after later runs.

A CampaignRun stores:
- campaign
- start/end time
- final status
- total/completed/failed districts
- records found/saved

CampaignRunDistrict snapshots the district-level result for that run:
- district
- status
- attempts
- records found/saved
- start/end time
- last error

This supports a History screen such as:
Bookseller — India — Completed — 780/780 districts — 125,420 records — View / Export.

History is run-oriented. Detailed per-field change auditing is intentionally postponed.
