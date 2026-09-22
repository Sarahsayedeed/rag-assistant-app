import pytest
from fastapi.testclient import TestClient
from app.main import app

class MockCollection:
    def count(self):
        return 10

class MockRetrievalService:
    def __init__(self):
        self.collection = MockCollection()

    def retrieve(self, question: str):
        return [
            {"text": "Mock context", "source": "test.pdf", "page": 1, "distance": 0.5}
        ]

class MockClient:
    def list(self):
        pass

class MockGenerationService:
    def __init__(self):
        self.client = MockClient()

    def generate(self, question: str, contexts: list):
        return "This is a mock answer.", ["test.pdf (p. 1)"]

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        # Setup mocks after lifespan has run
        app.state.retrieval_service = MockRetrievalService()
        app.state.generation_service = MockGenerationService()
        yield test_client

def test_query_happy_path(client):
    response = client.post("/query", json={"question": "What is AI?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is a mock answer."
    assert "test.pdf (p. 1)" in data["sources"]

def test_query_blank_question(client):
    response = client.post("/query", json={"question": "   "})
    assert response.status_code == 422

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["vector_store_count"] == 10
    assert data["ollama_status"] == "ok"
