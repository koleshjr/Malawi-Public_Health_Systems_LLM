import os 
import torch
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_community.llms import HuggingFaceHub, CTransformers
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
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

        elif self.model_provider == "hf_local":
            # if a folder that stores these models locally does not exist
            if not os.path.exists("src/models"):
                os.makedirs("src/models")
                model_id  = self.model_name
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = AutoModelForCausalLM.from_pretrained(model_id, low_cpu_mem_usage=True, torch_dtype=torch.float16)
                model.save_pretrained("src/models/" + model_id + "-model")
                tokenizer.save_pretrained("src/models/" + model_id + "-tokenizer")
                del model 
                del tokenizer
                torch.cuda.empty_cache()

                tokenizer = AutoTokenizer.from_pretrained("src/models/" + model_id + "-tokenizer")
                model = AutoModelForCausalLM.from_pretrained("src/models/" + model_id + "-model", low_cpu_mem_usage=True, torch_dtype=torch.float16)
                pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=1000)
                hf  = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature': 0})
                return hf
            else:
                tokenizer = AutoTokenizer.from_pretrained("src/models/" + self.model_name + "-tokenizer")
                model = AutoModelForCausalLM.from_pretrained("src/models/" + self.model_name + "-model", low_cpu_mem_usage=True, torch_dtype=torch.float16)
                pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=1000)
                hf  = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature': 0})
                return hf
        elif self.model_provider == "ctransformers":
            local_llm = "src/models/zephyr-7b-alpha.Q4_0.gguf"
            config = {
                "max_new_tokens": 512,
                "repetition_penalty": 1.1,
                "temperature": 0,
                "top_k": 50,
                "top_p": 0.95,
                "stream": True,
                "threads": int(os.cpu_count() / 2),
            }
            llm = CTransformers(
                model = local_llm,
                config = config
            )

            return llm
            

        else:
            raise Exception("Invalid model provider we currently support only ollama")
        