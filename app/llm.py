from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.chat_message_histories import RedisChatMessageHistory

from app.pinecone_client import pinecone_client


class LLMSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo')
        self.message_history = RedisChatMessageHistory(
            url="redis://localhost:6379/0", ttl=600, session_id=self.session_id
        )
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            chat_memory=self.message_history,
            return_messages=True,
            input_key='question',
            output_key='answer',
        )
        self.question_answer = ConversationalRetrievalChain.from_llm(
            self.llm,
            pinecone_client.retriever,
            memory=self.memory,
            chain_type='stuff',
            return_source_documents=True,
        )

    def query(self, query):
        result = self.question_answer({'question': query})
        source_urls = [doc.metadata['url'] for doc in result['source_documents']]
        # preserve order, but remove duplicates
        seen = set()
        source_urls = [url for url in source_urls if not (url in seen or seen.add(url))]

        return {'answer': result['answer'], 'source_urls': source_urls}


if __name__ == '__main__':
    llm_session = LLMSession('testing')
    query = 'Does glossgenius offer a card reader?'

    # Track token usage
    with get_openai_callback() as cb:
        print(llm_session.query(query))
        print(cb)
