from langchain_community.embeddings import OllamaEmbeddings, GPT4AllEmbeddings, FastEmbedEmbeddings, HuggingFaceBgeEmbeddings, HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import torch

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
        elif self.embedding_provider == 'huggingface':
            model_name =  "BAAI/bge-small-en"
            model_kwargs = {"device": "cpu"}
            encode_kwargs = {"normalize_embeddings": True}
            hf = HuggingFaceBgeEmbeddings(
                model_name = model_name,
                model_kwargs = model_kwargs,
                encode_kwargs = encode_kwargs,
            )
            return hf
        elif self.embedding_provider == 'sentence':
            if not os.path.exists("src/embedding_models"):
                os.makedirs("src/embedding_models")
                model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
                model.save("src/embedding_models/all-mpnet-base-v2")
                del model
                torch.cuda.empty_cache()
                encode_kwargs = {'normalize_embeddings': False}
                embedding_model_instance = HuggingFaceEmbeddings(
                    model_name = "src/embedding_models/all-mpnet-base-v2",
                    encode_kwargs = encode_kwargs,
                )
                return embedding_model_instance
            
            else:
                encode_kwargs = {'normalize_embeddings': False}
                embedding_model_instance = HuggingFaceEmbeddings(
                    model_name = "src/embedding_models/all-mpnet-base-v2",
                    encode_kwargs = encode_kwargs,
                )
                return embedding_model_instance

        else:
            raise Exception("Invalid embedding provider we currently support only openai and google embeddings")
        