from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Process and vectorize uploaded PDF document into Chroma vector store
def process_pdf_file(file_path):
    try:
        # Load raw text content from the target PDF file
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Split document text into manageable chunks for embedding generation
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_docs = text_splitter.split_documents(docs)

        # Generate HuggingFace embeddings and persist document chunks in Chroma DB
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        Chroma.from_documents(split_docs, embeddings, persist_directory="./chroma_db")

        # Return success payload on completion
        return {"status": "success", "message": "PDF processed successfully!"}
    except Exception as e:
        # Catch runtime errors and return failure response
        return {"status": "error", "message": str(e)}