import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def ask(question: str) -> dict:
    url = f"{API_BASE_URL}/query"
    try:
        response = requests.post(
            url,
            json={"question": question},
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Failed to connect to the backend API."}
    except requests.exceptions.Timeout:
        return {"error": "The request to the backend API timed out."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error occurred: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

def check_health() -> dict:
    url = f"{API_BASE_URL}/health"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {"status": "healthy"}
    except requests.exceptions.RequestException:
        return {"status": "unhealthy"}
