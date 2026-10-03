from app.orchestrator import district_pipeline
def test_default_pipeline_does_not_require_osm():
    assert "OSMOverpassAdapter()" not in __import__("inspect").getsource(district_pipeline.process_district)
