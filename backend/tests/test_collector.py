from app.collector.deduplicator import deduplicate
from app.collector.normalizer import normalize_email, normalize_name, normalize_phone, normalize_website
from app.collector.types import RawEntity

def test_normalization():
    assert normalize_name("  ABC Book House ")=="abc book house"
    assert normalize_phone("+91 98765 43210")=="9876543210"
    assert normalize_email(" INFO@EXAMPLE.COM ")=="info@example.com"
    assert normalize_website("example.com")=="https://example.com"

def test_deduplicate():
    a=RawEntity(name="ABC Book House",pin="841226",phone="+91 9876543210",source_name="a",source_url="https://a")
    b=RawEntity(name="ABC  Book House",pin="841226",phone="9876543210",source_name="b",source_url="https://b")
    assert len(deduplicate([a,b]))==1
