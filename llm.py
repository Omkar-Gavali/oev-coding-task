from langchain_groq import ChatGroq
from config import GROQ_API_KEY

def get_llm():
    if not GROQ_API_KEY:
        raise ValueError("❌ Error: GROQ_API_KEY is missing! Set it in the .env file.")
    return ChatGroq(api_key=GROQ_API_KEY)
