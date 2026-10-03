from app.sources.search_settings import SearchSettings,SearchMode
from app.sources.web_search import search_web_diagnostic
def test_search_failure_is_visible(monkeypatch):
    monkeypatch.setattr("app.sources.web_search.search_engine",lambda *a,**k:(_ for _ in ()).throw(RuntimeError("captcha blocked")))
    d={};rows=search_web_diagnostic("schools",SearchSettings(google=True,bing=False,yahoo=False,mode=SearchMode.ALL),d)
    assert rows==[] and d["google"].status=="blocked" and d["google"].error
