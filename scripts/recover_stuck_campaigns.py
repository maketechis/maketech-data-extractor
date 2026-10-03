from sqlalchemy import select
from app.database import SessionLocal
from app.models.core import Campaign,CampaignLocation,CampaignStatus,LocationStatus
def main():
    with SessionLocal() as db:
        campaigns=db.scalars(select(Campaign).where(Campaign.status==CampaignStatus.RUNNING)).all();fixed=0
        for campaign in campaigns:
            locations=db.scalars(select(CampaignLocation).where(CampaignLocation.campaign_id==campaign.id)).all()
            if not locations or any(x.status in (LocationStatus.RUNNING,LocationStatus.COLLECTING,LocationStatus.ENRICHING) for x in locations):continue
            if any(x.status==LocationStatus.PENDING for x in locations):
                campaign.status=CampaignStatus.FAILED
                for x in locations:
                    if x.status==LocationStatus.PENDING:
                        x.status=LocationStatus.FAILED;x.last_error="Recovered after interrupted/aborted campaign transaction. Create a new campaign to retry."
                fixed+=1
        db.commit();print({"campaigns_recovered":fixed})
if __name__=="__main__":main()
