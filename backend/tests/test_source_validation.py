from app.source_extraction.validation import filter_records
def test_rejects_generic_and_non_school_rows():
    rows=[{"name":"Institutions","source_url":"x"},{"name":"Bihar School Examination Board, Patna","source_url":"x"},{"name":"Orbit Public School","source_url":"x"}]
    good,stats=filter_records(rows,district="Siwan",state="Bihar")
    assert [x["name"] for x in good]==["Orbit Public School"]
    assert stats["rejected"]==2
def test_strips_search_engine_as_website():
    rows=[{"name":"Alpha Public School","website":"https://www.google.com/maps/place/x","source_url":"x"}]
    good,_=filter_records(rows,district="Siwan",state="Bihar")
    assert good[0]["website"] is None
