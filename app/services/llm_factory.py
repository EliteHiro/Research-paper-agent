import os
from langchain_groq import ChatGroq
from app.config.settings import get_settings

settings = get_settings()

def get_llm():
    """
    Returns an LLM instance with automatic fallbacks based on available API keys.
    Order of preference: Groq -> Gemini -> Anthropic -> OpenAI
    """
    models = []
    
    # 1. Primary: Groq (Fastest)
    groq_key = os.environ.get("GROQ_API_KEY") or settings.GROQ_API_KEY
    if groq_key:
        models.append(ChatGroq(
            model=settings.MODEL_NAME,
            api_key=groq_key,
            temperature=0.1,
            max_retries=1
        ))
        
    # 2. Fallback: Google Gemini
    gemini_key = os.environ.get("GOOGLE_API_KEY")
    if gemini_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        models.append(ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            api_key=gemini_key,
            temperature=0.1,
            max_retries=1
        ))
        
    # 3. Fallback: Anthropic
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        from langchain_anthropic import ChatAnthropic
        models.append(ChatAnthropic(
            model="claude-3-haiku-20240307",
            api_key=anthropic_key,
            temperature=0.1,
            max_retries=1
        ))
        
    # 4. Fallback: OpenAI
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        from langchain_openai import ChatOpenAI
        models.append(ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_key,
            temperature=0.1,
            max_retries=1
        ))

    if not models:
        raise ValueError("No API keys found. Please provide at least one valid LLM API key.")

    # If only one model is available, return it directly
    if len(models) == 1:
        return models[0]
        
    # Otherwise, chain them with fallbacks!
    # If the first model hits a rate limit (429) or fails, LangChain tries the next one.
    primary_model = models[0]
    fallback_models = models[1:]
    
    return primary_model.with_fallbacks(fallback_models)
