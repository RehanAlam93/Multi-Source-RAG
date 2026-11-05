from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def process_youtube_video(video_id):
    try:
        # Using the standard method call for the latest youtube-transcript-api
        # fetch() takes the video ID directly or via instance depending on version
        try:
            # Method 1: Using instance (as in your original solo code)
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.fetch(video_id, languages=['hi', 'en'])
            transcript_data = transcript_list.to_raw_data()
            transcript_text = "\n".join([item['text'] for item in transcript_data])
        except Exception:
            # Method 2: Fallback to list method if instance fails
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi', 'en'])
            transcript_text = " ".join([item['text'] for item in transcript_list])

        if not transcript_text:
            return {"status": "error", "message": "No transcript found for this video."}

        # Split text into chunks for RAG
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.create_documents([transcript_text])

        # Embeddings & Chroma Vector Store storage
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

        return {"status": "success", "message": "YouTube video processed successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}