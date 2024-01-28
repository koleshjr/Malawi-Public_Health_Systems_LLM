import os 
from langchain_community.embeddings import OllamaEmbeddings, GPT4AllEmbeddings, FastEmbedEmbeddings
from dotenv import load_dotenv

class Embeddings:
    def __init__(self, embedding_provider: str):
        load_dotenv()
        self.embedding_provider = embedding_provider

    def get_embedding_function(self):
        if self.embedding_provider == 'qdrant':
            return FastEmbedEmbeddings()
        elif self.embedding_provider == 'gpt4all':
            return GPT4AllEmbeddings()
        elif self.embedding_provider == 'ollama':
            return OllamaEmbeddings()
        else:
            raise Exception("Invalid embedding provider we currently support only openai and google embeddings")
        