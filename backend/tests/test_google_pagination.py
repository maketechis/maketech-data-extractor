from app.sources.google_direct import search_google_pages
def test_google_pages_requests_five_pages(monkeypatch):
    calls=[]
    monkeypatch.setattr("app.sources.google_direct.search_google_page",lambda q,page,limit=10,timeout=20:(calls.append(page) or []))
    search_google_pages("school list siwan",pages=5)
    assert calls==[1,2,3,4,5]
