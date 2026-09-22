from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logging_config import setup_logging
from app.core.config import settings, validate_config
from app.api.routes import query
from app.services.retrieval import RetrievalService
from app.services.generation import GenerationService

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_config()
    app.state.retrieval_service = RetrievalService()
    app.state.generation_service = GenerationService()
    yield
    # Cleanup if needed

app = FastAPI(title="RAG Assistant API", lifespan=lifespan)

origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)
