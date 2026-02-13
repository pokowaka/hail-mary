import logging
from .base import LLMClient
from gemini.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

class GeminiWrapper(LLMClient):
    def __init__(self, model: str = "gemini-2.5-flash"):
        super().__init__()
        self.client = GeminiClient(model=model)

    async def get_generated_text(self, prompt: str) -> str:
        self.last_prompt = prompt
        logger.debug(f"Sending prompt to Gemini: {prompt[:100]}...")
        response = await self.client.get_generated_text(prompt)
        self.last_response = response
        logger.debug(f"Received response from Gemini: {response[:100]}...")
        return response
