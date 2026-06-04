from langchain_groq import ChatGroq

from app.config.settings import get_settings


settings = get_settings()


def get_llm():

    return ChatGroq(
        model=settings.MODEL_NAME,
        api_key=settings.GROQ_API_KEY,
        temperature=0.1
    )
