from fastapi import FastAPI
from app.api.campaigns import router as campaigns_router
from app.api.geography import router as geography_router
from app.api.collector import router as collector_router
from app.api.jobs import router as jobs_router

app = FastAPI(
    title="MakeTech Data Extractor",
    version="0.3.0",
    description="District-wise entity collection and enrichment platform",
)
app.include_router(geography_router)
app.include_router(campaigns_router)
app.include_router(collector_router)
app.include_router(jobs_router)

@app.get("/")
def root():
    return {"name": "MakeTech Data Extractor", "version": "0.3.0"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": "development",
        "system": {
            "orchestrator": "implemented",
            "collector": "implemented",
            "enricher": "pending",
        },
    }
