import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# General Settings
PDF_PATH = os.getenv("PDF_PATH", "./data/test.pdf")
JSON_PATH = os.getenv("JSON_PATH", "./data/test.json")
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "./db")

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Vector Store
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "my_collection")

# Server Settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
