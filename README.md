# RAG-based System with FastAPI, LangChain, and ChromaDB

## Overview
This project implements a **Retrieval Augmented Generation (RAG) system** that utilizes a **Language Model (LLM), a vector database (ChromaDB), and FastAPI** to answer queries based on a given document. The system relies **only on the provided document** (not the LLM's built-in knowledge) and retrieves relevant information from a **PDF file (`test.pdf`) and a JSON file (`test.json`).**

✅ **Retrieves information only from provided documents**  
✅ **Uses FastAPI to serve an API for querying**  
✅ **Stores and retrieves data using ChromaDB**  
✅ **Uses Hugging Face sentence embeddings**  

---

## 🛠️ Tech Stack
- **Language Model**: Integrated via Groq API
- **Embeddings**: `sentence-transformers/all-mpnet-base-v2`
- **Vector Database**: ChromaDB
- **API Framework**: FastAPI
- **PDF Processing**: PyMuPDF
- **JSON Parsing**: Python `json` module
- **Environment**: Python 3.12+, VS Code

---

## 🚀 Installation & Setup
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/Omkar-Gavali/oev-coding-task.git
cd oev-coding-task
```

### **2️⃣ Create and Activate a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file and add the following:
```ini
GROQ_API_KEY=your_api_key_here
PERSIST_DIRECTORY=./db
PDF_PATH=test.pdf
JSON_PATH=test.json
```

---

## 🏗️ How It Works
1. **Data Ingestion**:
   - Extracts text from `test.pdf` and `test.json`.
   - Splits text into smaller chunks for better retrieval.
   - Stores embeddings in **ChromaDB**.

2. **Query Processing**:
   - User sends a query via FastAPI.
   - The retriever searches ChromaDB for relevant document chunks.
   - The LLM generates an answer using retrieved data.

---

## 🚦 Running the Project

### **1️⃣ Ingest Data into ChromaDB**
```sh
python ingest.py
```

### **2️⃣ Start FastAPI Server**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **3️⃣ Query the API**
#### Example Request:
```sh
curl "http://localhost:8000/query?question=What is block chain?"
```

#### Example Response:
```json
{
  "answer": "AI stands for Artificial Intelligence...",
  "sources": ["Page 1"],
  "additional_metadata": ["File: test.pdf"]
}
```

---

## 📝 API Endpoints
| Method | Endpoint | Description |
|--------|-------------|----------------|
| `GET`  | `/query?question=...` | Query the system for an answer |

---

## 🐳 Running with Docker (Optional)
1. **Build Docker Image**
```sh
docker build -t rag-system .
```

2. **Run Container**
```sh
docker run -p 8000:8000 rag-system
```

---

## 🛠️ Troubleshooting
**1️⃣ FastAPI Not Running?**  
🔹 Ensure you have activated the virtual environment:  
```sh
source venv/bin/activate  # Windows: venv\Scripts\activate
```
🔹 Check if `uvicorn` is installed:
```sh
pip install uvicorn
```

**2️⃣ Getting API Key Errors?**  
🔹 Make sure `.env` file is set up correctly and restart your terminal.

**3️⃣ Vector Store Not Working?**  
🔹 Delete the `./db` folder and re-run `python ingest.py`.

---

