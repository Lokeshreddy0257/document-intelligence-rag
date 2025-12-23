"""
Configuration settings for the Document Intelligence RAG System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-4"
TEMPERATURE = 0.0

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
COLLECTION_NAME = "document_collection"

# Document Processing Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SEPARATORS = ["\n\n", "\n", " ", ""]

# Retrieval Configuration
TOP_K = 4
SIMILARITY_THRESHOLD = 0.7

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Streamlit Configuration
STREAMLIT_THEME = "dark"
PAGE_TITLE = "Document Intelligence RAG"
PAGE_ICON = "📚"
