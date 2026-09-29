from app.sources.policy import SourcePurpose,build_source_plan

def test_school_entity_list_prefers_dataset_import():
    plan=build_source_plan(entity_type="school",country_iso="IN",purpose=SourcePurpose.ENTITY_LIST)
    assert [x.slug for x in plan]==["csv"]

def test_school_supplemental_discovery_uses_osm():
    plan=build_source_plan(entity_type="school",country_iso="IN",purpose=SourcePurpose.SUPPLEMENTAL_DISCOVERY)
    assert [x.slug for x in plan]==["osm"]

def test_paid_disabled_by_default():
    assert all(x.cost=="free" for x in build_source_plan(entity_type="school",country_iso="IN",purpose=SourcePurpose.ENTITY_LIST))
