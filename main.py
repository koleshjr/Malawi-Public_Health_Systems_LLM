import argparse
from src.services.retrieval import Retrieval
from src.services.embeddings import Embeddings
from src.services.llms import Llms
from src.helpers.config import Config
from src.helpers.utils import prepare_train_examples, load_test_data
from langchain_core.runnables import ConfigurableField 


parser = argparse.ArgumentParser(description='retrieval and generation')
parser.add_argument('--vector_store', type=str, default='chroma', help='vector store')
parser.add_argument('--index_name', type=str, default='index', help='index name')
parser.add_argument('--model_provider', type=str, default='huggingface', help='model provider')
parser.add_argument('--model_name', type=str, default='', help='model name')
parser.add_argument('--embedding_provider', type=str, default='huggingface', help='embedding provider')
args = parser.parse_args()



if __name__ == "__main__":
    examples = prepare_train_examples(train_filepath=Config.train_filepath)
    df_sub = load_test_data(test_filepath=Config.test_filepath)
    llm = Llms(model_provider=args.model_provider, model_name=args.model_name).get_chat_model()
    retrieval = Retrieval(vector_store=args.vector_store, index_name=args.index_name)
    embeddings = Embeddings(embedding_provider=args.embedding_provider)
    formatted_examples = "\n\n        ".join(examples.tolist())

    for row in df_sub.itertuples():
        try:
            print("<--------------------------------------------------------------------------------------->")
            print(f"Query: {row._2}")  # Access the second element by index
            print()
            
            answer = retrieval.retrieve_and_generate(embedding_function=embeddings.get_embedding_function(), query=row._2, examples=formatted_examples, template=Config.malawi_template, llm=llm)
            print(f"Answer: {answer}")
            print()

            print("<--------------------------------------------------------------------------------------->")
        except Exception as e:
            print(f"Error: {e} in row: {row}")

        break
