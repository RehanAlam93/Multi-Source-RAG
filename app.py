import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate

from utils.youtube_loader import process_youtube_video
from utils.pdf_loader import process_pdf_file
from utils.web_loader import process_website_url

# Load environment variables from .env configuration file
load_dotenv()
# Initialize Flask application instance
app = Flask(__name__)

# Configure upload directory for incoming PDF documents
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Groq LLM instance with strict model specification
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.3, groq_api_key=groq_api_key)

# Route to render the main frontend interface
@app.route('/')
def index():
    return render_template('index.html')

# Route to process and ingest YouTube video transcript data
@app.route('/process-youtube', methods=['POST'])
def handle_youtube():
    data = request.get_json()
    video_id = data.get('video_id')
    result = process_youtube_video(video_id)
    return jsonify(result)

# Route to handle PDF file uploads, local saving, and text indexing
@app.route('/process-pdf', methods=['POST'])
def handle_pdf():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected"})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    result = process_pdf_file(file_path)
    return jsonify(result)

# Route to scrape and process content from a target website URL
@app.route('/process-web', methods=['POST'])
def handle_web():
    data = request.get_json()
    url = data.get('url')
    result = process_website_url(url)
    return jsonify(result)

# Route to handle RAG chat queries using vector retrieval and LLM response generation
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get('query')

        # Load Chroma Vector Store and configure MMR retriever for optimal context
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 5})

        retrieved_docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        # Define structured prompt template with multi-language matching support
        prompt_template = PromptTemplate(
            input_variables=["context", "query"],
            template="""You are a helpful AI assistant. Read the provided context carefully and answer the question accurately.
If the answer is not present in the context, politely state that it is not mentioned in the source material.
Match the language of the user's query (if they ask in Hindi/Hinglish, reply in Hindi/Hinglish; if in English, reply in English). Keep it natural.

Context:
{context}

User Query: {query}
Answer:"""
        )

        formatted_prompt = prompt_template.format(context=context, query=query)
        response = llm.invoke(formatted_prompt)
        answer = response.content if hasattr(response, 'content') else str(response)

        return jsonify({"status": "success", "answer": answer})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Run the Flask web application server on port 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)