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
parser.add_argument('--index_name', type=str, default='index', help='index name')
parser.add_argument('--model_provider', type=str, default='huggingface', help='model provider')
parser.add_argument('--model_name', type=str, default='', help='model name')
parser.add_argument('--embedding_provider', type=str, default='huggingface', help='embedding provider')
parser.add_argument('--continue_training', type=bool, default=False, help='continue training')
args = parser.parse_args()



if __name__ == "__main__":
    if args.continue_training:
        print("Continuing training")
        df_sub = pd.read_csv('src/competition_data/submission_mistral_progress.csv')
        print(df_sub['answer'].isnull().sum())
    else:
        df_sub = load_test_data(test_filepath=Config.test_filepath)
    
    llm = Llms(model_provider=args.model_provider, model_name=args.model_name).get_chat_model()
    retrieval = Retrieval(vector_store=args.vector_store, index_name=args.index_name)
    embeddings = Embeddings(embedding_provider=args.embedding_provider)


    # Assuming df_sub is your DataFrame
    for row in df_sub.itertuples():
        if pd.isna(row.answer):
            try:
                print("<--------------------------------------------------------------------------------------->")
                print(f"Query: {row._2}")  # Access the second element by index
                print()

                answer = retrieval.retrieve_and_generate(embedding_function=embeddings.get_embedding_function(), query=row._2, template=Config.malawi_template, llm=llm)

                # Check if 'answer' is a list of dictionaries
                if isinstance(answer, list) and all(isinstance(item, dict) for item in answer):
                    # Assume the first element in the list is the relevant one
                    answer = answer[0]

                # Try the new extraction method
                answer_properties = answer.get('properties', None)
                if answer_properties:
                    answer = {
                        'answer': answer_properties.get('answer', None),
                        'filename': answer_properties.get('filename', None),
                        'paragraph': answer_properties.get('paragraph', None),
                        'keywords': answer_properties.get('keywords', None)
                    }
                else:
                    # Fallback to the previous extraction method
                    answer = {
                        'answer': answer.get('answer', None),
                        'filename': answer.get('filename', None),
                        'paragraph': answer.get('paragraph', None),
                        'keywords': answer.get('keywords', None)
                    }

                print(f"Answer: {answer['answer']}")
                print()

                # Update the DataFrame with the new values
                df_sub.loc[row.Index, 'answer'] = answer['answer']
                df_sub.loc[row.Index, 'filename'] = answer['filename']
                df_sub.loc[row.Index, 'paragraph'] = answer['paragraph']
                df_sub.loc[row.Index, 'keywords'] = answer['keywords']

                # Save the updated DataFrame to CSV
                df_sub.to_csv("src/competition_data/submission_mistral_progress.csv", index=False)
                print("<--------------------------------------------------------------------------------------->")
            except Exception as e:
                print(f"Error: {e} in row: {row}")
        else:
            print(f"Skipping row: {row.Index} as it has already been answered")

    # Assuming prepare_submit_files is a function that processes df_sub
    prepare_submit_files(df_sub).to_csv("src/competition_data/submission_full_mistral.csv", index=False)
