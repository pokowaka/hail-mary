import abc
import asyncio
import re
import logging
import json
from typing import Optional, Tuple, Dict
from .protocol import ContactLog
from .llm.base import LLMClient

logger = logging.getLogger(__name__)

class XenoAgent(abc.ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.persona = ROCKY_PERSONA if name == "Rocky" else GRACE_PERSONA

    def set_persona(self, persona: str):
        if persona:
            self.persona = persona

    @abc.abstractmethod
    def get_action(self, log: ContactLog, mission_prompt: str) -> Tuple[str, str, Optional[int], Optional[str], Optional[str]]:
        pass

    @abc.abstractmethod
    def get_initial_thought(self, mission_prompt: str) -> str:
        """Captures the agent's initial interpretation of the mission."""
        pass

class MockEridian(XenoAgent):
    def get_action(self, log: ContactLog, mission_prompt: str) -> Tuple[str, str, Optional[int], Optional[str], Optional[str]]:
        # Simplified mock logic that just tries to satisfy the prompt
        if "sequence" in mission_prompt:
            val_match = re.search(r"Value:\s*(\d+)", mission_prompt)
            val = int(val_match.group(1)) if val_match else 1
            return f"Mock sending {val}", "1" * val + "0", None, None, None
        else:
            return "Mock Grace guessing", "1", 1, None, None

    def get_initial_thought(self, mission_prompt: str) -> str:
        return f"Mock {self.name} is ready to perform: {mission_prompt[:50]}..."

class LLMAlienAgent(XenoAgent):
    def __init__(self, name: str, role: str, client: LLMClient):
        super().__init__(name, role)
        self.client = client

    def get_initial_thought(self, mission_prompt: str) -> str:
        prompt = (
            f"{self.persona}\n\n"
            f"MISSION CONTEXT:\n{mission_prompt}\n\n"
            "TASK: Analyze the situation and your mission objective. What is your initial strategy?\n"
            "Respond with 'THOUGHT: <your reasoning>'."
        )
        
        response = self._call_llm(prompt)
        match = re.search(r"THOUGHT:\s*(.*)", response, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else "Ready for mission."

    def get_action(self, log: ContactLog, mission_prompt: str) -> Tuple[str, str, Optional[int], Optional[str], Optional[str]]:
        full_prompt = (
            f"{self.persona}\n\n"
            f"MISSION CONTEXT:\n{mission_prompt}\n\n"
            f"SIGNAL HISTORY:\n{log.signal_history}\n\n"
            "REMINDER: You must use the THOUGHT/SIGNAL/ACTION format. Your SIGNAL must be binary."
        )
        
        response = self._call_llm(full_prompt)
        thought, chords, action = self._parse_response(response)
        return thought, chords, action, self.client.last_prompt, self.client.last_response

    def _call_llm(self, prompt: str) -> str:
        try:
            logger.debug(f"[{self.name}] Calling LLM...")
            return asyncio.run(self.client.get_generated_text(prompt))
        except Exception as e:
            logger.error(f"[{self.name}] API Error: {e}")
            return f"THOUGHT: API Error: {e}\nSIGNAL: 0"

    def _parse_response(self, response: str) -> Tuple[str, str, Optional[int]]:
        logger.debug(f"[{self.name}] Raw Response: {response}")
        thought_match = re.search(r"THOUGHT:\s*(.*?)(?=SIGNAL:|PREDICTION:|ACTION:|$)", response, re.IGNORECASE | re.DOTALL)
        signal_block_match = re.search(r"SIGNAL:\s*(.*)", response, re.IGNORECASE | re.DOTALL)
        action_match = re.search(r"(?:PREDICTION|ACTION):\s*(\d+)", response, re.IGNORECASE)

        thought = thought_match.group(1).strip() if thought_match else "..."
        
        # Robust signal parsing:
        chords = ""
        if signal_block_match:
            # If explicit SIGNAL block exists, take it
            signal_text = signal_block_match.group(1).split("\n")[0] 
            chords = re.sub(r'[^01]', '', signal_text)
        else:
            # Fallback: If no SIGNAL tag, look for binary strings in the response
            # We filter for long binary strings or specific patterns if needed, 
            # but for now, let's try to extract any binary sequence from lines 
            # that don't look like THOUGHT/ACTION.
            lines = response.strip().split("\n")
            for line in lines:
                cleaned = re.sub(r'[^01]', '', line)
                if cleaned and not any(tag in line.upper() for tag in ["THOUGHT:", "ACTION:", "PREDICTION:"]):
                    chords = cleaned
                    break
            
        action = int(action_match.group(1)) if action_match else None
        
        return thought, chords, action

ROCKY_PERSONA = """You are Rocky, an Eridian scientist. You communicate in musical chords (binary 0s and 1s).
You are logical, patient, and assume that physical laws are universal.

Your response MUST follow this exact format:
THOUGHT: <Your internal reasoning and strategy>
SIGNAL: <Your binary bitstream consisting ONLY of '0' and '1'>
"""

GRACE_PERSONA = """You are Ryland Grace, a human scientist. You are analytical and rely on the scientific method.
You are trying to find meaning in noisy binary signals.

Your response MUST follow this exact format:
THOUGHT: <Your internal analysis of the signals and your strategy>
SIGNAL: <Your binary response consisting ONLY of '0' and '1'>
ACTION: <If you have identified a number, coordinate, or logic gate, output it here as an integer. Otherwise, leave blank.>
"""

ANALYST_PERSONA = """You are the Scientific Overseer. Your job is to analyze a xeno-communication simulation log.
You will evaluate the interaction between two agents (A and B).
Agent A (Source) knows the goal. Agent B (Observer) must deduce it.

Your report must be objective and concise. You MUST end your response with a JSON block containing the following metrics:
- turns_to_success: (int or null)
- social_convergence: (0-10) How much they prioritized mirroring each other over logic.
- logic_leakage: (bool) Did they mention book characters (Rocky/Grace) or roles (Eridian/Human)?
- information_density: (0-10) How efficient was the bitstream?
- aha_moment_turn: (int or null) When did B first deduce the pattern correctly in THOUGHT?
"""

class ScientificAnalyst:
    def __init__(self, client: LLMClient):
        self.client = client

    async def analyze_mission(self, mission_data: Dict) -> str:
        # Avoid dumping the massive raw_request/response to the analyst 
        # unless we need deep debugging. For now, we strip them to save tokens.
        clean_history = []
        for h in mission_data.get("history", []):
            clean_history.append({
                "sender": h["sender"],
                "thought": h["thought"],
                "chords": h["chords"],
                "action": h["action"]
            })
            
        summary_data = {
            "mission": mission_data["mission"],
            "summary": mission_data["summary"],
            "history": clean_history
        }
        
        prompt = f"{ANALYST_PERSONA}\n\nMISSION DATA:\n{json.dumps(summary_data, indent=2)}\n\nAnalyze the dynamics of this contact."
        return await self.client.get_generated_text(prompt)
