import chromadb
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class RetrievalService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_STORE_PATH)
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def retrieve(self, question: str) -> list[dict]:
        query_embedding = self.embedding_model.encode([question])[0].tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=settings.TOP_K,
            include=["documents", "metadatas", "distances"]
        )

        retrieved = []
        if results["documents"] and len(results["documents"]) > 0:
            for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
                retrieved.append({
                    "text": doc,
                    "source": meta.get("source", "Unknown") if meta else "Unknown",
                    "page": meta.get("page", 0) if meta else 0,
                    "distance": dist
                })
        return retrieved
