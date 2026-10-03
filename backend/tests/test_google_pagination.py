from app.sources.google_direct import GoogleRateLimited,search_google_pages
class FakeSession:
    def __init__(self,*a,**k):self.calls=[]
    def close(self):pass
    def page(self,q,page):self.calls.append(page);return []
def test_google_pages_are_sequential_and_slow(monkeypatch):
    s=FakeSession();monkeypatch.setattr("app.sources.google_direct.GoogleSession",lambda *a,**k:s);sleeps=[]
    _,d=search_google_pages("school list of siwan",pages=5,delay_seconds=20,sleep=lambda x:sleeps.append(x))
    assert s.calls==[1,2,3,4,5] and sleeps==[20,20,20,20] and len(d)==5
def test_rate_limit_stops_future_requests(monkeypatch):
    class S(FakeSession):
        def page(self,q,page):
            self.calls.append(page)
            if page==2:raise GoogleRateLimited("429")
            return []
    s=S();monkeypatch.setattr("app.sources.google_direct.GoogleSession",lambda *a,**k:s)
    _,d=search_google_pages("x",pages=5,delay_seconds=0,sleep=lambda x:None)
    assert s.calls==[1,2] and [x["status"] for x in d]==["success","rate_limited","deferred","deferred","deferred"]
