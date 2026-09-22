import logging
import ollama
from app.core.config import settings

logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self):
        self.client = ollama.Client(host=settings.OLLAMA_HOST)
        self.model = settings.OLLAMA_MODEL

    def generate(self, question: str, contexts: list[dict]) -> tuple[str, list[str]]:
        if not contexts:
            return "I could not find this in the provided documents.", []

        context_text = ""
        sources = []
        for i, ctx in enumerate(contexts, 1):
            source_info = f"{ctx['source']} (p. {ctx['page']})"
            context_text += f"[{i}] {ctx['text']}\n(Source: {ctx['source']}, Page: {ctx['page']})\n\n"
            if source_info not in sources:
                sources.append(source_info)
        
        prompt = (
            "You are a helpful document assistant. Your job is to answer questions based on the context provided.\n"
            "Instructions:\n"
            "- Answer using ONLY the information from the context blocks below.\n"
            "- The question may use different words or phrasing than the context. Look for semantic matches, not just exact keywords.\n"
            "- If the context contains relevant information even in a different language or phrasing, use it to answer.\n"
            "- Cite your sources using [1], [2], etc. matching the context block numbers.\n"
            "- If the context truly does not contain any relevant information, say: \"I could not find this in the provided documents.\"\n"
            "- Keep your answer concise and direct.\n\n"
            "Context:\n"
            f"{context_text}"
            f"Question: {question}\n\n"
            "Answer:\n"
        )

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": 0,
                    "num_predict": 512,
                    "num_ctx": 4096,
                }
            )
            return response.get("response", ""), sources
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise RuntimeError("Failed to connect to the generation service") from e
