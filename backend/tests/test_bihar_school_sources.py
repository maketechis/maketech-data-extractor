from app.services.bihar_school_sources import fetch_bssb
def test_bssb_parser(monkeypatch):
    html="<table><tr><td>1</td><td>Siwan</td><td>Test Sanskrit School</td><td>10123456789</td><td>माध्यमिक</td></tr></table>"
    class R:
        text=html
        def raise_for_status(self):pass
    monkeypatch.setattr("app.services.bihar_school_sources.httpx.get",lambda *a,**k:R())
    rows=fetch_bssb("Siwan")
    assert len(rows)==1 and rows[0].udise_code=="10123456789"
