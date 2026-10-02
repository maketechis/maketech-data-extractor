from app.models.core import Campaign
from app.schemas.campaign import CampaignCreate
def test_campaign_create_accepts_search_settings():
    p=CampaignCreate(name="Siwan",entity_type_id=1,country_id=1,search_google=True,search_bing=False,search_yahoo=True,search_mode="fallback")
    c=Campaign(**p.model_dump())
    assert c.search_google is True
    assert c.search_bing is False
    assert c.search_yahoo is True
    assert c.search_mode=="fallback"
