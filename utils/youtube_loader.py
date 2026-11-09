from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Fetch transcript from YouTube video, split text into chunks, and store vector embeddings in Chroma DB
def process_youtube_video(video_id):
    try:
        # Attempt to retrieve transcript using multiple fallback methods for version compatibility
        try:
            # Method 1: Using YouTubeTranscriptApi instance fetch method for Hindi and English languages
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.fetch(video_id, languages=['hi', 'en'])
            transcript_data = transcript_list.to_raw_data()
            transcript_text = "\n".join([item['text'] for item in transcript_data])
        except Exception:
            # Method 2: Fallback to static get_transcript method if instance method fails
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
            transcript_text = " ".join([item['text'] for item in transcript_list])

        # Validate if transcript text was successfully retrieved
        if not transcript_text:
            return {"status": "error", "message": "No transcript found for this video."}

        # Split transcript text into structured chunks for RAG processing
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.create_documents([transcript_text])

        # Generate HuggingFace embeddings and store chunks in the persistent Chroma vector store
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

        # Return success payload on completion
        return {"status": "success", "message": "YouTube video processed successfully!"}
    except Exception as e:
        # Catch transcript extraction or vectorization errors and return failure response
        return {"status": "error", "message": str(e)}