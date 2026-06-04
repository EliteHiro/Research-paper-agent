from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    GROQ_API_KEY: str = ""

    MODEL_NAME: str = "llama-3.3-70b-versatile"

    MAX_CHUNK_SIZE: int = 4000

    CHUNK_OVERLAP: int = 500

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


@lru_cache
def get_settings():
    return Settings()
