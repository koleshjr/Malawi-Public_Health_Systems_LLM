import argparse
import pandas as pd
from src.services.retrieval import Retrieval
from src.services.embeddings import Embeddings
from src.services.llms import Llms
from src.helpers.config import Config
from src.helpers.utils import load_test_data, prepare_submit_files
from langchain_core.runnables import ConfigurableField 


parser = argparse.ArgumentParser(description='retrieval and generation')
parser.add_argument('--vector_store', type=str, default='chroma', help='vector store')
parser.add_argument('--index_name', type=str, default='chroma_bge', help='index name')
parser.add_argument('--embedding_provider', type=str, default='huggingface', help='embedding provider')
parser.add_argument('--data_type', type = str, help='either train or test' )
args = parser.parse_args()



if __name__ == "__main__":
    if args.data_type == "train":
        df = pd.read_csv(Config.train_filepath)
        output_path = "src/output/train_with_rag.csv"
    else:
        df = pd.read_csv(Config.test_filepath)
        output_path = "src/output/test_with_rag.csv"
    # llm = Llms(model_provider=args.model_provider, model_name=args.model_name).get_chat_model()
    retrieval = Retrieval(vector_store=args.vector_store, index_name=args.index_name)
    embeddings = Embeddings(embedding_provider=args.embedding_provider)

    print(len([col for col in df['Question Text'].unique() if 'Compare' in col]))

    for index, row in df.iterrows():
        try:
            print("<--------------------------------------------------------------------------------------->")
            print(f"Query: {row['Question Text']}")  # Access the second element by index
            print()
   
            answer = retrieval.retrieve_only(embedding_function=embeddings.get_embedding_function(), query=row['Question Text'])
            # Build the string answer
            string_answer = '\n'.join([f"Context {i+1}: {doc.page_content}, Reference: {doc.metadata['source']}, Paragraph: {doc.metadata['paragraph']}" for i, doc in enumerate(answer)])
            # Print the string answer
            # print(string_answer)
            # print(f"Answer: {string_answer}")
            # print(f"Actual: {row['Question Answer']}")
            # print(f'Paragraph: {row["Paragraph(s) Number"]}')
            # print(f'reference document: {row["Reference Document"]}')
            print()

            df.at[index, 'retrived_context'] = string_answer
            df.to_csv(output_path, index=False)
            print("<--------------------------------------------------------------------------------------->")
        except Exception as e:
            print(f"Error: {e} in row: {row}")
        
        




    
