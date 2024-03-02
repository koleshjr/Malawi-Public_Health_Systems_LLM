import os 
from langchain_community.document_loaders import CSVLoader

class DocumentLoader:
    def __init__(self):
        pass

    def load_and_get_text(self, folder_path: str):
        docs = """"""

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                if file_path.endswith(".csv"):
                    loader = CSVLoader(file_path)
                    data = loader.load()
                    print(data)

                    context = "\n\n".join(str(p.page_content) for p in data)
                    docs += context
            except Exception as e:
                print(f"Error loading file {file} with error {e}") 

        return docs

                

