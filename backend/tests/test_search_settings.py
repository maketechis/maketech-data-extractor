from app.sources.search_settings import SearchMode,SearchSettings

def test_checkbox_engine_selection():
    s=SearchSettings(google=True,bing=False,yahoo=True,mode=SearchMode.FALLBACK)
    assert s.enabled_engines()==["google","yahoo"]

def test_all_engines_default_enabled():
    assert SearchSettings().enabled_engines()==["google","bing","yahoo"]
