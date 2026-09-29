from app.sources.google_direct import build_google_query

def test_google_query_is_geography_scoped():
    assert build_google_query(entity_type="bookseller",district="Siwan",state="Bihar",country="India")=="bookseller Siwan Bihar India"
    assert build_google_query(entity_type="school",district="Siwan",state="Bihar",country="India",name="St Joseph School")=='"St Joseph School" Siwan Bihar India'
