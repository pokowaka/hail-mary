import abc
from typing import Optional

class LLMClient(abc.ABC):
    def __init__(self):
        self.last_prompt: Optional[str] = None
        self.last_response: Optional[str] = None

    @abc.abstractmethod
    async def get_generated_text(self, prompt: str) -> str:
        """Sends a prompt to the LLM and returns the text response."""
        pass
