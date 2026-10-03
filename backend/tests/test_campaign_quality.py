from app.orchestrator.full_campaign import _quality
def test_low_coverage_is_degraded():
    source={"discovery":{"query":"school list","pages":5,"results":0,"sources_saved":0},"extraction":{"sources":0,"raw":0,"accepted":0,"saved":0,"failed_sources":0}}
    result={"collection":{"raw":0},"enrichment":{}}
    q=_quality(source,result,0)
    assert q["status"]=="degraded" and q["score"]<40
def test_dense_sources_raise_quality():
    source={"discovery":{"query":"school list","pages":5,"results":40,"sources_saved":35},"extraction":{"sources":35,"raw":100,"accepted":80,"saved":70,"failed_sources":2}}
    result={"collection":{"raw":20},"enrichment":{"complete":10}}
    q=_quality(source,result,2)
    assert q["status"]=="healthy" and q["duplicates_merged"]==2 and q["google_pages"]==5
