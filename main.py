import argparse
from src.services.retrieval import Retrieval
from src.services.embeddings import Embeddings
from src.services.llms import Llms
from src.helpers.config import Config
from src.helpers.utils import load_test_data, prepare_submit_files, extract_info

from langchain_core.runnables import ConfigurableField 


parser = argparse.ArgumentParser(description='retrieval and generation')
parser.add_argument('--vector_store', type=str, default='chroma', help='vector store')
parser.add_argument('--index_name', type=str, default='index', help='index name')
parser.add_argument('--model_provider', type=str, default='huggingface', help='model provider')
parser.add_argument('--model_name', type=str, default='', help='model name')
parser.add_argument('--embedding_provider', type=str, default='huggingface', help='embedding provider')
args = parser.parse_args()



if __name__ == "__main__":
    df_sub = load_test_data(test_filepath=Config.test_filepath)
    llm = Llms(model_provider=args.model_provider, model_name=args.model_name).get_chat_model()
    retrieval = Retrieval(vector_store=args.vector_store, index_name=args.index_name)
    embeddings = Embeddings(embedding_provider=args.embedding_provider)


    for row in df_sub.itertuples():
        try:
            print("<--------------------------------------------------------------------------------------->")
            query = f'<s>[INST] Question: {row.question} \n{row.retrived_context} [/INST]'
            print(f"Query: {query}")  # Access the second element by index
            print()
   
            answer = retrieval.answer_already_retrieved(query=query, llm=llm)
            print(f"Answer: {answer}")
            print()

            df_sub.loc[row.Index, 'answer'] = answer


            df_sub.to_csv(f"src/competition_data/submission_{args.model_name}_progress.csv", index=False)
            print("<--------------------------------------------------------------------------------------->")
        except Exception as e:
            print(f"Error: {e} in row: {row}")
    df_sub['filename'], df_sub['paragraph'], df_sub['keywords'] = zip(*df_sub['answer'].apply(extract_info))
    prepare_submit_files(df_sub).to_csv("src/competition_data/submission_gemini.csv", index=False)

    
