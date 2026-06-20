import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_llm():
    """
    Returns an LLM instance with automatic fallbacks based on available API keys.
    
    Priority order: Groq -> Gemini
    If Groq hits a rate limit or fails, it seamlessly falls back to Gemini.
    """
    models = []
    active_providers = []

    # 1. Primary: Groq (Fastest)
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    if groq_key:
        try:
            from langchain_groq import ChatGroq
            models.append(ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=groq_key,
                temperature=0.1,
                max_retries=0  # Don't retry on rate limit — fall through to next provider
            ))
            active_providers.append("Groq")
        except Exception as e:
            logger.warning(f"Failed to initialize Groq: {e}")

    # 2. Fallback: Google Gemini
    gemini_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            models.append(ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                api_key=gemini_key,
                temperature=0.1,
                max_retries=0
            ))
            active_providers.append("Gemini")
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini: {e}")

    if not models:
        raise ValueError(
            "No LLM API keys found! Please provide at least one key "
            "(GROQ_API_KEY or GOOGLE_API_KEY) "
            "in the Streamlit secrets or .env file."
        )

    logger.info(f"Active LLM providers: {' -> '.join(active_providers)}")

    # If only one model is available, return it directly
    if len(models) == 1:
        return models[0]

    # Chain them with fallbacks
    primary = models[0]
    fallbacks = models[1:]

    return primary.with_fallbacks(fallbacks)


def get_active_providers() -> list[str]:
    """Returns a list of provider names that have valid API keys configured."""
    providers = []
    if os.environ.get("GROQ_API_KEY", "").strip():
        providers.append("Groq")
    if os.environ.get("GOOGLE_API_KEY", "").strip():
        providers.append("Gemini")
    return providers
