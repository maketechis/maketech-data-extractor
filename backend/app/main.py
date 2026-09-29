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
from app.api.history import router as history_router
from app.api.sources import router as sources_router
from app.api.geography_validation import router as geography_validation_router
from app.api.source_policy import router as source_policy_router
from app.api.google_discovery import router as google_discovery_router
from app.api.search_settings import router as web_search_router
from app.config import get_settings

settings=get_settings()
app=FastAPI(title=settings.app_name,version="0.5.0",description="District-wise entity collection and enrichment platform")
for router in (geography_router,campaigns_router,collector_router,jobs_router,campaign_control_router,enrichment_router,verification_router,enrichment_jobs_router,pipeline_router,exports_router,history_router,sources_router,geography_validation_router,source_policy_router,google_discovery_router,web_search_router):
    app.include_router(router)

@app.get("/")
def root():
    return {"name":settings.app_name,"version":"0.5.0"}

@app.get("/health")
def health():
    return {"status":"ok","environment":settings.environment,"system":{"orchestrator":"implemented","collector":"implemented","enricher":"implemented","history":"implemented","exports":"implemented","source_registry":"implemented"}}
