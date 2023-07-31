import os

from dotenv import load_dotenv

# You can run prod by setting this i.e. ENV=prod python run.py
ENV = os.environ.get('ENV', 'dev')

if ENV == 'dev':
    ENV_PATH = os.environ.get('ENV_PATH', 'env/local-dev.env')
    load_dotenv(dotenv_path=ENV_PATH)


# load other env variables
DEBUG = os.environ.get("DEBUG") == 'true'
FRONTEND_TOKEN_SECRET_KEY = 'FRONTEND_TOKEN'
FRONTEND_TOKEN_SECRET = os.environ.get(FRONTEND_TOKEN_SECRET_KEY)
REDIS_URL = os.environ.get('REDIS_URL')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_ENV = os.environ.get('PINECONE_ENV')
PINECONE_INDEX_NAME = os.environ.get('PINECONE_INDEX_NAME')
