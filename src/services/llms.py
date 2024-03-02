import os 
import torch
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv

class Llms:
    def __init__(self, model_provider: str, model_name: Optional[str] = None):
        load_dotenv()
        self.model_provider = model_provider
        self.model_name = model_name

    def get_chat_model(self):
        if self.model_provider == 'ollama':
            return ChatOllama(model = self.model_name)
        elif self.model_provider == "hf_online":
            llm = HuggingFaceHub(
            repo_id=self.model_name, model_kwargs={"temperature": 0, "max_length": 264}
            )

            return llm

        elif self.model_provider == "openai":
            return ChatOpenAI(model=self.model_name, openai_api_key=os.getenv("OPENAI_API_KEY"))

        elif self.model_provider == 'google':
            return ChatGoogleGenerativeAI(model = self.model_name, google_api_key=os.getenv('GOOGLE_API_KEY'))

 


        else:
            raise Exception("Invalid model provider we currently support only ollama")
        