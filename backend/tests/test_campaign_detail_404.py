import pytest
from fastapi import HTTPException
from app.api.campaign_list import detail
class MissingDB:
    def get(self,model,key): return None
def test_missing_campaign_detail_returns_404():
    with pytest.raises(HTTPException) as exc:
        detail(999999,db=MissingDB())
    assert exc.value.status_code==404
