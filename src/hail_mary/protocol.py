from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

@dataclass
class Exchange:
    sender: str
    thought: str
    chords: str
    action: Optional[Any] = None # Renamed from prediction for generality
    raw_request: Optional[str] = None
    raw_response: Optional[str] = None

@dataclass
class ContactLog:
    mission_name: str
    history: List[Exchange] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def record_exchange(self, exchange: Exchange):
        self.history.append(exchange)

    @property
    def signal_history(self) -> str:
        # Formatted history for agent prompts using dynamic labels
        labels = self.metadata.get("labels", {})
        return " | ".join([f"{labels.get(e.sender, e.sender)}: {e.chords}" for e in self.history])

    @property
    def last_chords(self) -> str:
        return self.history[-1].chords if self.history else ""
