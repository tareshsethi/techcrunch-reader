# techcrunch-reader 

[This was a open-ended takehome (I chose the project). Spent a weekend on it] assistant for parsing through recent tech crunch articles, updated daily

### How to run

Install requirements

```
pip install -r requirements.txt
```

Add env variables, here's a list:

- DEBUG
- OPENAI_API_KEY
- PINECONE_ENV
- PINECONE_API_KEY
- PINECONE_INDEX_NAME
- REDIS_URL
- FRONTEND_TOKEN

Run redis, celery, backend, frontend in separate shells

```
redis-server
celery -A app.celery.celery worker -B --loglevel=info
python run.py
streamlit run frontend.py
```

### Architecture and Rationales

- OpenAI gpt-3.5-turbo LLM (10 times cheaper than text-davinci-003, fine to run via third party since data is not sensitive i.e. techcrunch data is public)
- OpenAI embeddings (Fast, no need to run embeddings locally since data is not sensitive)
- Langchain for glue code for prompting llm
  - ConversationalRetrievalChain connected to pinecone to parse through relevant documents, and prompt with the appropriate context
  - Uses ConversationBufferWindowMemory for handling memory for a session, storing the last 5 conversations
  - Returns sources for each chat bot answer, to make answers referencable
- Pinecone Vector Store (Simplest to use, offers free index, hosted - no need to host locally since data is not sensitive)
- Celery for scheduling daily tasks for techcrunch ingestion (and probably some future tasks for managing documents stored, or running llm offline)
- Redis (Celery store, LLM memory store)
- Streamlit frontend (hacked this up so I don't have to write frontend)
- Flask backend (lightweight)

### Next Steps

1. Understand document staleness - right now the vector db grows linearly every day with more documents, which not only results in more costs with storing the db, but also makes it harder for the QARetrieval chain, etc.

   - A solution here would involve some combination of deleting stale documents + prioritizing more relevant documents in the retrieval chain

2. Experiment and understand limitations of the llm solution itself. Known limitations include:

   - Sometimes struggles to find answer, and says I don’t know when the answer is in the documents
   - As of now, it is prompted to only retrieve answers from documents in the vector store, so it can't handle general purpose questions
     - A solution here would involve some combination of updating the ConversationalRetrievalChain prompt, use separate chains/agents to understand intent of the query and only use QA chain if applicableor
   - Some extra sources retrieved are not relevant to the query

3. I envision a product like this would be used to help VCs and individuals parse through new startups, so queries like “any startup worth investing in today”, or “can you build a comparison table of the startups mentioned today and what they do“ are target queries that don’t work right now in this toy implementation of a QA model. So, more generally speaking, this requires a lot more building towards product requirements and goals.

### Initial Design Sketch

<img width="574" alt="Screen Shot 2023-07-30 at 5 40 23 PM" src="https://github.com/tareshsethi/techcrunch-reader/assets/36555549/cbb02a15-e296-4172-802a-51b1505f17a6">
