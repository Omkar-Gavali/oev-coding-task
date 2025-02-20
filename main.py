from fastapi import FastAPI, Query
from vector_store import ingest_data, init_vector_store
from llm import get_llm
from langchain.chains import RetrievalQA

pdf_path = "test.pdf"  # Your PDF file path here

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
    response = qa_chain.run(question)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    #om
