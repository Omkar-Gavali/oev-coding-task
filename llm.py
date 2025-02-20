import os
from langchain.chat_models import ChatGroq

# Initialize LLM
def get_llm():
    return ChatGroq(api_key=os.getenv("GROQ_API_KEY"))
