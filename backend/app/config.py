from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_ENV=Path(__file__).resolve().parents[3]/".env"

class Settings(BaseSettings):
    app_name: str="MakeTech Data Extractor"
    environment: str="development"
    debug: bool=True
    database_url: str="sqlite:///:memory:"
    direct_url: str|None=None
    auth_secret: str="change-me-in-production"
    max_districts_per_campaign: int=1
    max_entities_per_district: int=100
    max_pages_per_domain: int=10
    max_retries: int=2
    request_delay_seconds: float=2.0
    enable_ai: bool=False
    enable_paid_search: bool=False
    enable_proxy: bool=False
    system_enabled: bool=True
    collector_enabled: bool=True
    enrichment_enabled: bool=True
    model_config=SettingsConfigDict(env_file=ROOT_ENV,env_file_encoding="utf-8",extra="ignore")

@lru_cache
def get_settings()->Settings:
    return Settings()
