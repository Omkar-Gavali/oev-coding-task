from fastapi import FastAPI, Query
from vector_store import ingest_data, init_vector_store
from llm import get_llm
from langchain.chains import RetrievalQA

pdf_path = "test.pdf"  # Your PDF file path here
json_path = "test.json"  # Your JSON file path here
# Initialize API
app = FastAPI()

# Load vector store
vector_db = init_vector_store()  # Load persisted DB
retriever = vector_db.as_retriever()

# Load LLM
llm = get_llm()

# Set up RAG pipeline
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

@app.get("/query")
def query(question: str = Query(..., description="Your question here")):
    retrieved_docs = retriever.get_relevant_documents(question)

    if not retrieved_docs:
        return {"answer": "No relevant information found."}

    sources = set()
    additional_metadata = set()

    for doc in retrieved_docs:
        if "page" in doc.metadata:
            sources.add(f"Page {doc.metadata['page']}")
        if "file_name" in doc.metadata:
            additional_metadata.add(f"File: {doc.metadata['file_name']}")  # Add file name

    response = qa_chain.run(question)

    return {
        "answer": response,
        "sources": list(sources),
        "additional_metadata": list(additional_metadata)  # Include file name
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

 

