from pathlib import Path
from app.config import ROOT_ENV

def test_root_env_points_to_repository_root():
    expected=Path(__file__).resolve().parents[2]/".env"
    assert ROOT_ENV==expected
