import datetime

import pinecone
import pytz
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

from app.env import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX_NAME

EMBEDDING_DIM = 1536


class PineConeClient:
    embeddings = OpenAIEmbeddings()

    def __init__(self):
        pinecone.init(
            api_key=PINECONE_API_KEY,  # find at app.pinecone.io
            environment=PINECONE_ENV,  # next to api key in console
        )

        self.docsearch = Pinecone.from_existing_index(
            PINECONE_INDEX_NAME, self.embeddings
        )
        self.retriever = self.docsearch.as_retriever(search_type="mmr")
        self.index = pinecone.Index(PINECONE_INDEX_NAME)
        self.vectorstore = Pinecone(self.index, self.embeddings.embed_query, "text")

    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)

    def get_last_updated_epoch_timestamp(self):
        """Looks for the latest document posted in the last 24 hours. If not found, returns 24 hours ago"""
        now = datetime.datetime.now(pytz.utc)
        yesterday = now - datetime.timedelta(hours=24)
        yesterday_epoch = yesterday.timestamp()
        documents = self.index.query(
            top_k=10000,
            vector=[0] * EMBEDDING_DIM,
            namespace='',
            include_metadata=True,
            filter={"epoch_timestamp": {"$gte": yesterday_epoch}},
        )['matches']
        if len(documents) == 0:
            return yesterday_epoch
        epoch_timestamps = [doc['metadata']['epoch_timestamp'] for doc in documents]
        latest = list(reversed(sorted(epoch_timestamps)))[0]
        return latest

    def get_all_vectors_stale(self, date):
        """Returns all stale vectors' ids, separated by commas, and the number of vectors found,
        so we can manually review and delete"""
        epoch_timestamp = date.timestamp()
        stale_documents = self.index.query(
            top_k=10000,
            vector=[0] * EMBEDDING_DIM,
            namespace='',
            filter={"epoch_timestamp": {"$lte": epoch_timestamp}},
        )['matches']
        vector_ids = [data['id'] for data in stale_documents]
        return ','.join(vector_ids), len(vector_ids)


pinecone_client = PineConeClient()
