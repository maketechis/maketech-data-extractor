from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.campaign_list import get_db
from app.database import Base
from app.main import app

def test_missing_campaign_detail_returns_404():
    engine=create_engine("sqlite:///:memory:",connect_args={"check_same_thread":False})
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    def override():
        db=Session()
        try: yield db
        finally: db.close()
    app.dependency_overrides[get_db]=override
    try:
        r=TestClient(app).get("/campaign-runs/999999")
        assert r.status_code==404
    finally:
        app.dependency_overrides.clear()
