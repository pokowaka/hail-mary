import os
from openai import AsyncOpenAI
from .base import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-4-turbo", api_key: str = None, base_url: str = None):
        self.model = model
        self.client = AsyncOpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url
        )

    async def get_generated_text(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class AnthropicClient(LLMClient):
    def __init__(self, model: str = "claude-3-opus-20240229", api_key: str = None):
        from anthropic import AsyncAnthropic
        self.model = model
        self.client = AsyncAnthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    async def get_generated_text(self, prompt: str) -> str:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class DeepSeekClient(OpenAIClient):
    def __init__(self, model: str = "deepseek-chat", api_key: str = None):
        super().__init__(
            model=model,
            api_key=api_key or os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
