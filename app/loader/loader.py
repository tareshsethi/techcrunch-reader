import json
import tempfile

from langchain.document_loaders import JSONLoader
from langchain.text_splitter import CharacterTextSplitter

from app.loader.scraper import TechCrunchScraper
from app.pinecone_client import pinecone_client


def metadata_func(record: dict, metadata: dict) -> dict:
    metadata['title'] = record.get('title')
    metadata['epoch_timestamp'] = record.get('epoch_timestamp')
    metadata['url'] = record.get('url')

    return metadata


class IncrementalTechCrunchLoader:
    web_scraper = TechCrunchScraper()

    def load(self, date, from_json=None):
        # TODO: add logging
        if not from_json:
            dataset = self.web_scraper.parse(date)
            tmp = tempfile.NamedTemporaryFile()
            name = tmp.name + '.json'
            with open(name, 'w') as f:
                json.dump(dataset, f)
            from_json = name

        loader = JSONLoader(
            from_json,
            jq_schema='.data[]',
            content_key='content',
            metadata_func=metadata_func,
        )
        raw_documents = loader.load()
        text_splitter = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0, separator='\n'
        )
        documents = text_splitter.split_documents(raw_documents)
        pinecone_client.add_documents(documents)
