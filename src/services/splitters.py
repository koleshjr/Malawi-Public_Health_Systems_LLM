from langchain.text_splitter import RecursiveCharacterTextSplitter

class Splitter:
    def __init__(self, splitter: str):
        self.splitter = splitter

    def split(self, docs: str, chunk_size: int = 512, chunk_overlap: int = 64):
        if self.splitter == 'recursive':
            splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
            pages = splitter.split_text(docs)
            return splitter.create_documents(pages)
        else:
            raise Exception("Invalid splitter we currently support only recursive_character_splitter")