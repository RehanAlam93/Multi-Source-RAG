import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Define standard headers to mimic a real browser request and prevent blocking
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Fetch, parse, split, and vectorize text content from a target website URL into Chroma DB
def process_website_url(target_url):
    try:
        # Send HTTP GET request to fetch webpage content with a timeout limit
        response = requests.get(target_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return {"status": "error", "message": f"Failed to fetch URL. Status code: {response.status_code}"}

        # Parse HTML response and extract text from primary structural tags
        soup = BeautifulSoup(response.text, "html.parser")
        extracted_texts = []
        for element in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            text = element.get_text(strip=True)
            if text:
                extracted_texts.append(text)

        # Validate if any meaningful text was extracted from the webpage
        if not extracted_texts:
            return {"status": "error", "message": "No valid text content found."}

        # Combine all extracted paragraphs and headers into a single text body
        full_text = "\n".join(extracted_texts)

        # Split document text into structured chunks for embedding generation
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.create_documents([full_text])

        # Generate HuggingFace embeddings and persist the website chunks in Chroma vector store
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

        # Return success payload on completion
        return {"status": "success", "message": "Website URL processed successfully!"}
    except Exception as e:
        # Catch runtime or connection errors and return failure response
        return {"status": "error", "message": str(e)}