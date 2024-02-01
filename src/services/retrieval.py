import os
from typing import Optional
from operator import itemgetter
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma, Milvus, FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel 
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class RagOutput(BaseModel):
    answer: str = Field(description="The answer to the question")
    filename: str = Field(description="The filename of the document where the answer was found")
    paragraph: str = Field(description="The paragraph(s) Number where the answer was found")
    keywords: str = Field(description="Important comma separated keywords from the context where the answer was found")


class Retrieval:
    def __init__(self, vector_store, index_name, top_k: int = 1):
        load_dotenv()
        self.vector_store = vector_store
        self.index_name = "src/indexes/" + index_name 
        self.top_k = top_k

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def retrieve_and_generate(self, embedding_function: str, query: str, template: str, llm: str, with_sources: bool = False):
        parser = JsonOutputParser(pydantic_object=RagOutput)
        custom_rag_prompt = PromptTemplate(template = template, 
                                           input_variables = ["query", "context"],
                                           partial_variables = {"format_instructions": parser.get_format_instructions()},
        )

        if self.vector_store == 'chroma':
            vector_index = Chroma(persist_directory = self.index_name, embedding_function = embedding_function).as_retriever(search_type="similarity_score_threshold",
            search_kwargs={
                "k": self.top_k,
                "score_threshold": 0.5,
            },)
        elif self.vector_store == 'milvus':
            vector_index = Milvus(embedding_function, connection_args = {"host": os.getenv('MILVUS_HOST'), "port": os.getenv('MILVUS_PORT'), "collection_name": self.index_name}).as_retriever(search_kwargs = {"k": self.top_k})
        elif self.vector_store == 'faiss':
            vector_index = FAISS.load_local(self.index_name, embedding_function).as_retriever(search_kwargs = {"k": self.top_k})

        if not with_sources:
            rag_chain = (
                {"context": itemgetter("query") | vector_index,
                "query": itemgetter("query"),
                }
                | custom_rag_prompt
                | llm 
                # | StrOutputParser()
                | parser
            )
            return rag_chain.invoke({"query": query})
        
        else:
            rag_chain_from_docs = (
                RunnablePassthrough.assign(context = (lambda x: self.format_docs(x["context"])))
                | custom_rag_prompt
                | llm
                # | StrOutputParser()
                | parser
            )


            rag_chain_with_source = RunnableParallel(

                {"context": itemgetter("query") | vector_index,
                 "query": itemgetter("query"),
                }

            ).assign(answer = rag_chain_from_docs)

            return rag_chain_with_source.invoke({"query": query})

        