from app.sources.registry import compatible_sources

def test_bookseller_india_has_generic_sources():
    slugs={x.slug for x in compatible_sources(entity_type="bookseller",country_iso="IN")}
    assert {"csv","osm"}.issubset(slugs)

def test_unknown_type_still_supports_generic_csv():
    slugs={x.slug for x in compatible_sources(entity_type="hospital",country_iso="IN")}
    assert "csv" in slugs
