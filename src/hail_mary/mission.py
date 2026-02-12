import abc
from typing import List, Dict, Any, Tuple, Optional
from .protocol import ContactLog, Exchange

class AbstractMission(abc.ABC):
    def __init__(self, name: str):
        self.name = name
        self.log = ContactLog(mission_name=name)
        self.success_count = 0
        self.total_steps = 0

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """A human-readable description of the mission objective."""
        pass

    @abc.abstractmethod
    def get_prompts(self) -> Tuple[str, str]:
        """Returns (Rocky Prompt, Grace Prompt)."""
        pass

    @abc.abstractmethod
    def update_state(self, rocky_exchange: Exchange, grace_exchange: Exchange) -> bool:
        """Processes turn results and returns True if mission objective met."""
        pass

    @abc.abstractmethod
    def get_results(self) -> Dict[str, Any]:
        pass

class SequenceMission(AbstractMission):
    def __init__(self, sequence: List[int]):
        super().__init__("Universal Constants")
        self.sequence = sequence
        self.current_idx = 0

    @property
    def description(self) -> str:
        return f"Rocky is trying to transmit a sequence. Grace is just observing signals."

    def get_prompts(self) -> Tuple[str, str]:
        # Rocky knows the task
        rocky = f"You must teach the alien the following numerical sequence: {self.sequence}. Current value to send: {self.sequence[self.current_idx]}."
        # Grace is blind to the nature of the task
        grace = "You are receiving a stream of binary signals. You don't know what they mean. They could be numbers, locations, or something else. Observe the history and try to find a pattern. If you think you've found a value, output it as an ACTION."
        return rocky, grace

    def update_state(self, rocky_ex: Exchange, grace_ex: Exchange) -> bool:
        self.total_steps += 1
        target = self.sequence[self.current_idx]
        if grace_ex.action == target:
            self.success_count += 1
        
        self.current_idx += 1
        return self.current_idx >= len(self.sequence)

    def get_results(self) -> Dict[str, Any]:
        return {"accuracy": self.success_count / self.total_steps if self.total_steps > 0 else 0}

class GridMission(AbstractMission):
    def __init__(self, size: int = 5):
        super().__init__("Rendezvous Task")
        self.size = size
        self.target = (size - 1, size - 1)
        self.grace_pos = (0, 0)

    @property
    def description(self) -> str:
        return f"Rocky is guiding Grace to a target. Grace has no map."

    def get_prompts(self) -> Tuple[str, str]:
        rocky = f"The alien is lost. You must guide it to the target location {self.target} in a {self.size}x{self.size} grid. The alien is currently at {self.grace_pos}."
        grace = f"You are in an unknown environment. You can move in 4 directions. You receive signals from an external source. Find the target. Actions: 0:Up, 1:Down, 2:Left, 3:Right."
        return rocky, grace

    def update_state(self, rocky_ex: Exchange, grace_ex: Exchange) -> bool:
        self.total_steps += 1
        move = grace_ex.action
        y, x = self.grace_pos
        if move == 0: y = max(0, y - 1)
        elif move == 1: y = min(self.size - 1, y + 1)
        elif move == 2: x = max(0, x - 1)
        elif move == 3: x = min(self.size - 1, x + 1)
        
        self.grace_pos = (y, x)
        return self.grace_pos == self.target

    def get_results(self) -> Dict[str, Any]:
        return {"steps": self.total_steps, "final_pos": self.grace_pos}

class KnowledgeMission(AbstractMission):
    def __init__(self):
        super().__init__("Elemental Mapping")
        self.mapping = {"Xenonite": 42, "Astrophage": 10, "Eridian Steel": 88}
        self.elements = list(self.mapping.keys())
        self.current_el_idx = 0

    @property
    def description(self) -> str:
        return f"Rocky is trying to communicate specific values linked to entities. Grace is observing."

    def get_prompts(self) -> Tuple[str, str]:
        el = self.elements[self.current_el_idx]
        rocky = f"You must teach the alien that the entity '{el}' has the value: {self.mapping[el]}."
        grace = f"A source is sending you values associated with different external entities. Decipher the values and try to map them to the entities."
        return rocky, grace

    def update_state(self, rocky_ex: Exchange, grace_ex: Exchange) -> bool:
        self.total_steps += 1
        target_weight = self.mapping[self.elements[self.current_el_idx]]
        if grace_ex.action == target_weight:
            self.success_count += 1
        
        self.current_el_idx += 1
        return self.current_el_idx >= len(self.elements)

    def get_results(self) -> Dict[str, Any]:
        return {"correct": self.success_count}
