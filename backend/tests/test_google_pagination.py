from app.sources.google_direct import search_google_pages
def test_google_pages_requests_five_pages(monkeypatch):
    calls=[]
    monkeypatch.setattr("app.sources.google_direct.search_google_page",lambda q,page,limit=10,timeout=20:(calls.append(page) or []))
    rows,diagnostics=search_google_pages("school list siwan",pages=5)
    assert calls==[1,2,3,4,5] and len(diagnostics)==5
def test_one_google_page_failure_does_not_stop_other_pages(monkeypatch):
    def fake(q,page,limit=10,timeout=20):
        if page==2:raise RuntimeError("blocked")
        return []
    monkeypatch.setattr("app.sources.google_direct.search_google_page",fake)
    _,d=search_google_pages("x",pages=5)
    assert d[1]["status"]=="failed" and len(d)==5
