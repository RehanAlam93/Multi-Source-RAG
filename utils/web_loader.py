import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def process_website_url(target_url):
    try:
        response = requests.get(target_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return {"status": "error", "message": f"Failed to fetch URL. Status code: {response.status_code}"}

        soup = BeautifulSoup(response.text, "html.parser")
        extracted_texts = []
        for element in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            text = element.get_text(strip=True)
            if text:
                extracted_texts.append(text)

        if not extracted_texts:
            return {"status": "error", "message": "No valid text content found."}

        full_text = "\n".join(extracted_texts)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.create_documents([full_text])

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

        return {"status": "success", "message": "Website URL processed successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}