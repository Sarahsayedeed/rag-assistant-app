import logging
from fastapi import APIRouter, Request, HTTPException, status
from app.schemas.query import QueryRequest, QueryResponse
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

def get_retrieval_service(request: Request):
    return request.app.state.retrieval_service

def get_generation_service(request: Request):
    return request.app.state.generation_service

@router.get("/health")
def health_check(request: Request):
    try:
        retrieval_service = get_retrieval_service(request)
        count = retrieval_service.collection.count()
        vector_store_status = "ok"
    except Exception as e:
        logger.error(f"Vector store health check failed: {e}")
        count = 0
        vector_store_status = "error"

    try:
        gen_service = get_generation_service(request)
        gen_service.client.list()
        ollama_status = "ok"
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")
        ollama_status = "error"

    return {
        "status": "ok" if vector_store_status == "ok" and ollama_status == "ok" else "degraded",
        "vector_store_count": count,
        "ollama_status": ollama_status
    }

@router.post("/query", response_model=QueryResponse)
def handle_query(query_req: QueryRequest, request: Request):
    try:
        retrieval_service = get_retrieval_service(request)
        generation_service = get_generation_service(request)

        results = retrieval_service.retrieve(query_req.question)
        
        # Log distances for debugging
        if results:
            distances = [r["distance"] for r in results]
            logger.info(f"Query: '{query_req.question[:50]}...' | Distances: {distances}")
        
        # Always pass results to generation - let the LLM decide relevance
        # Only filter out truly irrelevant results (distance > threshold)
        filtered_results = [r for r in results if r["distance"] <= settings.DISTANCE_THRESHOLD]
        
        # If filtering removed everything but we had results, use top 3 anyway
        # This prevents "not found" when content exists but phrased differently
        if not filtered_results and results:
            filtered_results = results[:3]
            logger.info("Threshold filtered all results. Using top 3 as fallback.")
        
        answer, sources = generation_service.generate(query_req.question, filtered_results)
        
        return QueryResponse(answer=answer, sources=sources)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Language model service is unavailable."
        )
    except Exception as e:
        logger.error(f"Unexpected error during query processing: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
