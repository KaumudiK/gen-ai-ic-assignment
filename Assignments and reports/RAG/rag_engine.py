import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class RAGEngine:
    def __init__(self, documents_path='documents'):
        self.documents_path = documents_path
        self.vector_store = None
        self.embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2'
        )

    def load_documents(self):
        loader = DirectoryLoader(
            self.documents_path,
            glob='*.txt',
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        documents = loader.load()
        print(f"Loaded {len(documents)} documents")
        return documents

    def split_documents(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " "]
        )
        chunks = splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks

    def build_index(self):
        documents = self.load_documents()
        chunks = self.split_documents(documents)
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        print("Vector store built successfully")

    def search(self, query, top_k=3):
        if self.vector_store is None:
            return []
        results = self.vector_store.similarity_search(query, k=top_k)
        return results

    def generate_answer(self, query, top_k=3):
        chunks = self.search(query, top_k=top_k)

        if not chunks:
            return ("I couldn't find relevant information in the documents. "
                    "Please try rephrasing your question or contact HR directly.")

        context = "\n\n".join([chunk.page_content for chunk in chunks])

        sources = [chunk.metadata.get('source', 'Unknown') for chunk in chunks]
        unique_sources = list(set(sources))

        answer = (
            f"Based on the company documents, here's what I found:\n\n"
            f"{context}\n\n"
            f"**Sources:** {', '.join([os.path.basename(s) for s in unique_sources])}"
        )
        return answer