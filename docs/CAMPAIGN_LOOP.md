# Campaign loop

The campaign loop advances through persisted district jobs and isolates failures.

Development safety:
- API defaults to one district per invocation.
- API caps one invocation at 10 districts.
- Failed districts retry only below the configured attempt threshold.
- Pause prevents new districts from starting.
- A campaign is complete only when no pending/running districts remain and no failures remain.
- A campaign with exhausted failures is marked failed rather than silently reported complete.

A future worker/scheduler will repeatedly invoke the loop. Public OpenStreetMap endpoints must not be used for nationwide bulk campaigns.
