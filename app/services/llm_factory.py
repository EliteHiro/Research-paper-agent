from langchain_groq import ChatGroq

from app.config.settings import get_settings


settings = get_settings()


import os

def get_llm():
    # Fetch directly from os.environ to avoid import-time caching issues
    api_key = os.environ.get("GROQ_API_KEY") or settings.GROQ_API_KEY
    
    return ChatGroq(
        model=settings.MODEL_NAME,
        api_key=api_key,
        temperature=0.1
    )
