import datetime

from app.celery import celery
from app.loader.loader import IncrementalTechCrunchLoader
from app.pinecone_client import pinecone_client


@celery.task
def ingest_new_techcrunch_articles():
    last_updated = (
        pinecone_client.get_last_updated_epoch_timestamp()
        + datetime.timedelta(seconds=1)
    )
    loader = IncrementalTechCrunchLoader()
    loader.load(last_updated)
