import os
import json
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"
    VECTOR_STORE_PATH: str = "data/vector_store"
    COLLECTION_NAME: str = "documents"
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    TOP_K: int = 10
    DISTANCE_THRESHOLD: float = 0.9
    CORS_ORIGINS: str = "http://localhost:8501"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

import logging

logger = logging.getLogger(__name__)

settings = Settings()

def validate_config():
    """Validate that the configured embedding model matches the one used at indexing time."""
    config_path = os.path.join(settings.VECTOR_STORE_PATH, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            vector_store_config = json.load(f)
            if vector_store_config.get("embedding_model") and vector_store_config["embedding_model"] != settings.EMBEDDING_MODEL:
                raise ValueError(
                    f"Configured embedding model ({settings.EMBEDDING_MODEL}) does not match "
                    f"vector store model ({vector_store_config['embedding_model']})"
                )
        logger.info("Vector store config validated successfully.")
    else:
        logger.warning(f"Config file not found at {config_path}. Skipping validation.")

