from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import get_settings


settings = get_settings()


def chunk_text(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.MAX_CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

    return splitter.split_text(text)


def truncate_text(text: str, max_chars: int = 12000) -> str:
    """Truncate text to a maximum character count to avoid overwhelming the LLM."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[... remainder of paper truncated for brevity ...]"
