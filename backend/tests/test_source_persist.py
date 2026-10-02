from app.source_extraction.persist import ExtractedAdapter
def test_extracted_adapter_maps_raw_entity():
    x=ExtractedAdapter([{"name":"Alpha School","source_url":"https://x/list","source_record_id":"123"}]).collect()[0]
    assert x.name=="Alpha School" and x.source_name=="source_extraction" and x.source_record_id=="123"
