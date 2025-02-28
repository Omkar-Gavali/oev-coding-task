import json
import fitz  # PyMuPDF
import logging
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import PDF_PATH, JSON_PATH, PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load embeddings model
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Initialize Vector Store
def init_vector_store():
    embeddings = get_embeddings()
    return Chroma(collection_name=CHROMA_COLLECTION_NAME, embedding_function=embeddings, persist_directory=PERSIST_DIRECTORY)

# Process PDF files
def process_pdf(pdf_path):
    docs = []
    pdf_document = fitz.open(pdf_path)  # Open PDF
    file_name = os.path.basename(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text("text")

        if text.strip():
            docs.append({
                "content": text,
                "metadata": {"page": page_num + 1, "file_name": file_name}
            })

    return docs

# Process JSON files
def process_json(json_path):
    docs = []
    file_name = os.path.basename(json_path)

    with open(json_path, "r") as file:
        data = json.load(file)
        for idx, item in enumerate(data):
            docs.append({
                "content": json.dumps(item),
                "metadata": {"id": idx + 1, "file_name": file_name}
            })

    return docs

# Split text into smaller chunks
def split_documents(docs, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.create_documents(
        texts=[doc["content"] for doc in docs],
        metadatas=[doc["metadata"] for doc in docs]
    )

# Ingest data into ChromaDB
def ingest_data():
    logging.info(f"📥 Ingesting data from {PDF_PATH} and {JSON_PATH}...")
    vector_db = init_vector_store()
    
    pdf_docs = process_pdf(PDF_PATH)
    json_docs = process_json(JSON_PATH)
    all_docs = pdf_docs + json_docs

    if not all_docs:
        logging.warning("⚠️ No documents found! Check file paths.")
        return vector_db

    split_docs = split_documents(all_docs)
    vector_db.add_documents(split_docs)
    vector_db.persist()
    
    return vector_db
