import argparse
import warnings
from src.services.vector_databases import VectorStore
from src.services.document_loaders import DocumentLoader
from src.services.embeddings import Embeddings
from src.helpers.utils import prepare_context_data
from src.helpers.config import Config
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description= "index and embed required documents")
parser.add_argument('--vector_store', type=str, default='chroma')
parser.add_argument('--index_name', type=str, default='test_index')
parser.add_argument('--embedding_provider', type=str, default='huggingface')
args = parser.parse_args()

if __name__ == '__main__':
    loader = DocumentLoader()
    vector_store = VectorStore(args.vector_store, args.index_name)
    embedding_function = Embeddings(args.embedding_provider).get_embedding_function()
    df = prepare_context_data(Config.folder_path)   
    df.to_csv('src/data/context.csv', index=False)
    docs = loader.load_and_get_text(Config.folder_path)
    vector_store.store_embeddings(embedding_function, docs)
 