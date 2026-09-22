import chromadb
from app.core.config import settings

client = chromadb.PersistentClient(path=settings.VECTOR_STORE_PATH)
collection = client.get_collection(settings.COLLECTION_NAME)

data = collection.get(
    include=["documents", "metadatas"]
)

for doc, meta in zip(data["documents"], data["metadatas"]):
    text = doc.lower()

    if "where" in text or "having" in text:
        print("\n==============================")
        print("SOURCE:", meta.get("source"))
        print("PAGE:", meta.get("page"))
        print("TEXT:")
        print(doc)