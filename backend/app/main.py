from fastapi import FastAPI

app = FastAPI(
    title="MakeTech Data Extractor",
    version="0.1.0",
    description="District-wise entity collection and enrichment platform",
)

@app.get("/")
def root():
    return {"name": "MakeTech Data Extractor", "version": "0.1.0"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": "development",
        "system": {
            "orchestrator": "pending",
            "collector": "pending",
            "enricher": "pending",
        },
    }
