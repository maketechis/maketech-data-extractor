from fastapi import FastAPI
from app.api.campaigns import router as campaigns_router
from app.api.geography import router as geography_router
from app.api.collector import router as collector_router
from app.api.jobs import router as jobs_router
from app.api.campaign_control import router as campaign_control_router
from app.api.enrichment import router as enrichment_router
from app.api.verification import router as verification_router
from app.api.enrichment_jobs import router as enrichment_jobs_router
from app.api.pipeline import router as pipeline_router
from app.api.exports import router as exports_router

app = FastAPI(
    title="MakeTech Data Extractor",
    version="0.3.0",
    description="District-wise entity collection and enrichment platform",
)
app.include_router(geography_router)
app.include_router(campaigns_router)
app.include_router(collector_router)
app.include_router(jobs_router)
app.include_router(campaign_control_router)
app.include_router(enrichment_router)
app.include_router(verification_router)
app.include_router(enrichment_jobs_router)
app.include_router(pipeline_router)
app.include_router(exports_router)

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
