import os

from langchain_groq import ChatGroq

# Initialize LLM
def get_llm():
    return ChatGroq(api_key=os.getenv("GROQ_API_KEY"))
