import abc

class LLMClient(abc.ABC):
    @abc.abstractmethod
    async def get_generated_text(self, prompt: str) -> str:
        """Sends a prompt to the LLM and returns the text response."""
        pass
