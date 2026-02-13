from .base import LLMClient
from gemini.gemini_client import GeminiClient

class GeminiWrapper(LLMClient):
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.client = GeminiClient(model=model)

    async def get_generated_text(self, prompt: str) -> str:
        return await self.client.get_generated_text(prompt)
