from pydantic import BaseModel, Field

class CampaignCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    entity_type_id: int
    country_id: int
    collection_level: str = "district"
    search_google: bool = True
    search_bing: bool = True
    search_yahoo: bool = True
    search_mode: str = "fallback"

class CampaignRead(BaseModel):
    id: int
    name: str
    entity_type_id: int
    country_id: int
    collection_level: str
    status: str
    model_config = {"from_attributes": True}
