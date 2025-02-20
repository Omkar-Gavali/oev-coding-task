import json
import fitz
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import os


# Set up embeddings using Hugging Face
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Initialize Vector Store
def init_vector_store(persist_directory="./db"):
    embeddings = get_embeddings()
    return Chroma(collection_name="test_stores", embedding_function=embeddings, persist_directory=persist_directory)

# Load PDF and extract text
def process_pdf(pdf_path):
    docs = []
    pdf_document = fitz.open(pdf_path)  # Open PDF

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text("text")  # Extract text

        if text.strip():  # Only store non-empty pages
            docs.append({"content": text, "metadata": {"page": page_num + 1}})

    return docs

# Load JSON file
def process_json(json_path):
    docs = []
    with open(json_path, "r") as file:
        data = json.load(file)
        for idx, item in enumerate(data):
            docs.append({"content": json.dumps(item), "metadata": {"id": idx + 1}})
    return docs

# Function to split text into chunks
def split_documents(docs, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    formatted_docs = [doc["content"] for doc in docs]
    return text_splitter.create_documents(formatted_docs, metadatas=[doc["metadata"] for doc in docs])

# Ingest data into ChromaDB
def ingest_data(pdf_path="test.pdf", json_path="test.json", persist_directory="./db"):
    vector_db = init_vector_store(persist_directory)
    
    # Process documents
    pdf_docs = process_pdf(pdf_path)
    json_docs = process_json(json_path)
    all_docs = pdf_docs + json_docs

    # Chunking the documents
    split_docs = split_documents(all_docs)

    # Add documents to vector DB
    vector_db.add_documents(split_docs)
    vector_db.persist()  # Save to disk

    return vector_db
    