from fastapi import FastAPI, Query
from vector_store import init_vector_store
from llm import get_llm
from langchain.chains import RetrievalQA
import asyncio
from config import HOST, PORT

app = FastAPI()

# Load vector store
vector_db = init_vector_store()
retriever = vector_db.as_retriever()

# Load LLM
llm = get_llm()

# Set up RAG pipeline
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

@app.get("/query")
async def query(question: str = Query(..., description="Your question here")):
    loop = asyncio.get_running_loop()

    # Fetch relevant documents asynchronously
    retrieved_docs = await loop.run_in_executor(None, retriever.get_relevant_documents, question)

    if not retrieved_docs:
        return {"answer": "No relevant information found."}

    sources = set()
    additional_metadata = set()

    for doc in retrieved_docs:
        if "page" in doc.metadata:
            sources.add(f"Page {doc.metadata['page']}")
        if "file_name" in doc.metadata:
            additional_metadata.add(f"File: {doc.metadata['file_name']}")

    # Call LLM asynchronously
    response = await loop.run_in_executor(None, qa_chain.run, question)

    return {
        "answer": response,
        "sources": list(sources),
        "additional_metadata": list(additional_metadata)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
