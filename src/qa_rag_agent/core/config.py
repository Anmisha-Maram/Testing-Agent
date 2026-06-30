"""Application configuration placeholders for the QA RAG Agent."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Minimal settings scaffold for environment-driven configuration."""

    app_name: str = "qa-rag-agent"
    env_file: str = ".env"

    class Config:
        env_file = ".env"
        extra = "ignore"
