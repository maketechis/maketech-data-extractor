from app.orchestrator.full_campaign import _quality
def test_low_coverage_is_degraded():
    source={"discovery":{"sources":0,"engines":{"google":{"status":"blocked"}}},"extraction":{"raw_records":0}}
    result={"collection":{"raw":3},"enrichment":{"needs_discovery":3}}
    q=_quality(source,result,0)
    assert q["status"]=="degraded" and q["score"]<40
def test_dense_sources_raise_quality():
    source={"discovery":{"sources":4,"engines":{"bing":{"status":"success"}}},"extraction":{"raw_records":100}}
    result={"collection":{"raw":20},"enrichment":{"complete":10}}
    q=_quality(source,result,2)
    assert q["status"]=="healthy" and q["duplicates_merged"]==2
