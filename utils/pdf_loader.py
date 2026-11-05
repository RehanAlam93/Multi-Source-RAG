from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf_file(file_path):
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_docs = text_splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        Chroma.from_documents(split_docs, embeddings, persist_directory="./chroma_db")

        return {"status": "success", "message": "PDF processed successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}