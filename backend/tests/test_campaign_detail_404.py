from fastapi.testclient import TestClient
from app.main import app
def test_missing_campaign_detail_returns_404():
    r=TestClient(app).get("/campaign-runs/999999")
    assert r.status_code==404
