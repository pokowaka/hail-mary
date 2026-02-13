import abc
import asyncio
import re
from typing import Optional, Tuple
from .protocol import ContactLog

try:
    from gemini.gemini_client import GeminiClient
except ImportError:
    GeminiClient = None

class XenoAgent(abc.ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.persona = ROCKY_PERSONA if name == "Rocky" else GRACE_PERSONA

    def set_persona(self, persona: str):
        if persona:
            self.persona = persona

    @abc.abstractmethod
    def get_action(self, log: ContactLog, mission_prompt: str) -> Tuple[str, str, Optional[int]]:
        pass

    @abc.abstractmethod
    def get_initial_thought(self, mission_prompt: str) -> str:
        """Captures the agent's initial interpretation of the mission."""
        pass

class MockEridian(XenoAgent):
    def get_action(self, log: ContactLog, mission_prompt: str) -> Tuple[str, str, Optional[int]]:
        # Simplified mock logic that just tries to satisfy the prompt
        if "sequence" in mission_prompt:
            val_match = re.search(r"Value:\s*(\d+)", mission_prompt)
            val = int(val_match.group(1)) if val_match else 1
            return f"Mock sending {val}", "1" * val + "0", None
        else:
            return "Mock Grace guessing", "1", 1

    def get_initial_thought(self, mission_prompt: str) -> str:
        return f"Mock {self.name} is ready to perform: {mission_prompt[:50]}..."

class GeminiEridian(XenoAgent):
    def __init__(self, name: str, role: str, model_name: str = "gemini-2.5-flash"):
        super().__init__(name, role)
        self.client = GeminiClient(model=model_name) if GeminiClient else None

    def get_initial_thought(self, mission_prompt: str) -> str:
        prompt = f"{self.persona}\n\nMISSION CONTEXT:\n{mission_prompt}\n\nTASK: Analyze the situation and your mission objective. What is your initial strategy? Respond with ONLY your internal thought process starting with 'THOUGHT:'."
        
        response = self._call_llm(prompt)
        match = re.search(r"THOUGHT:\s*(.*)", response, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else "Ready for mission."

    def get_action(self, log: ContactLog, mission_prompt: str) -> Tuple[str, str, Optional[int]]:
        full_prompt = f"{self.persona}\n\nMISSION CONTEXT:\n{mission_prompt}\n\nSIGNAL HISTORY:\n{log.signal_history}"
        
        response = self._call_llm(full_prompt)
        return self._parse_response(response)

    def _call_llm(self, prompt: str) -> str:
        if not self.client:
            return "THOUGHT: Error: GeminiClient not found.\nSIGNAL: 0"
        try:
            return asyncio.run(self.client.get_generated_text(prompt))
        except Exception as e:
            return f"THOUGHT: API Error: {e}\nSIGNAL: 0"

    def _parse_response(self, response: str) -> Tuple[str, str, Optional[int]]:
        thought_match = re.search(r"THOUGHT:\s*(.*?)(?=SIGNAL:|PREDICTION:|ACTION:|$)", response, re.IGNORECASE | re.DOTALL)
        signal_match = re.search(r"SIGNAL:\s*([01\s]+)", response, re.IGNORECASE)
        # Handle both PREDICTION and ACTION keywords
        action_match = re.search(r"(?:PREDICTION|ACTION):\s*(\d+)", response, re.IGNORECASE)

        thought = thought_match.group(1).strip() if thought_match else "..."
        chords = re.sub(r'\s+', '', signal_match.group(1)) if signal_match else ""
        action = int(action_match.group(1)) if action_match else None
        
        return thought, chords, action

ROCKY_PERSONA = """You are Rocky, an Eridian. You communicate in binary musical chords.
You are extremely logical but have no concept of human language or culture.
Use THOUGHT for your reasoning and SIGNAL for your 0/1 bitstream."""

GRACE_PERSONA = """You are Ryland Grace, a human scientist. 
You are trying to communicate with an alien using binary signals.
Use THOUGHT for your analysis, ACTION for your numerical guess/prediction, and SIGNAL for your 0/1 response."""
