import abc
from typing import List, Dict, Any, Tuple, Optional
from .protocol import ContactLog, Exchange

class AbstractMission(abc.ABC):
    def __init__(self, name: str):
        self.name = name
        self.log = ContactLog(mission_name=name)
        self.success_count = 0
        self.total_steps = 0
        self.rocky_override = None
        self.grace_override = None

    def set_overrides(self, rocky: str = None, grace: str = None):
        self.rocky_override = rocky
        self.grace_override = grace

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """A human-readable description of the mission objective."""
        pass

    def get_prompts(self) -> Tuple[str, str]:
        """Returns (Rocky Prompt, Grace Prompt), applying overrides if present."""
        rocky, grace = self._get_task_prompts()
        return (self.rocky_override or rocky, self.grace_override or grace)

    @abc.abstractmethod
    def _get_task_prompts(self) -> Tuple[str, str]:
        """Subclasses implement this to define default prompts."""
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

    def _get_task_prompts(self) -> Tuple[str, str]:
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

    def _get_task_prompts(self) -> Tuple[str, str]:
        rocky = f"The alien is lost. You must guide it to the target location {self.target} in a {self.size}x{self.size} grid. The alien is currently at {self.grace_pos}."
        grace = "You can perform actions 0, 1, 2, or 3. After each action, you receive a signal. What is the source trying to convey? Discern the relationship between actions and signals."
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

    def _get_task_prompts(self) -> Tuple[str, str]:
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

class TimeMission(AbstractMission):
    def __init__(self, interval: int = 4):
        super().__init__("Temporal Sync")
        self.interval = interval

    @property
    def description(self) -> str:
        return f"Synchronize clocks. Rocky's pulse interval is {self.interval} units."

    def _get_task_prompts(self) -> Tuple[str, str]:
        rocky = f"Teach your unit of time. Send a '1' exactly every {self.interval} signals."
        grace = "Observe the signal bursts. What is the repeating interval between '1's? Output your guess as an ACTION."
        return rocky, grace

    def update_state(self, rocky_ex: Exchange, grace_ex: Exchange) -> bool:
        self.total_steps += 1
        if grace_ex.action == self.interval:
            self.success_count += 1
        return self.total_steps >= 5

    def get_results(self) -> Dict[str, Any]:
        return {"sync_success": self.success_count > 0}

class LogicMission(AbstractMission):
    def __init__(self, operator: str = "AND"):
        super().__init__(f"Logic Gate: {operator}")
        self.operator = operator
        self.test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.current_case = 0

    @property
    def description(self) -> str:
        return f"Establish fundamental binary logic: {self.operator}."

    def _get_task_prompts(self) -> Tuple[str, str]:
        a, b = self.test_cases[self.current_case]
        res = 0
        if self.operator == "AND": res = a & b
        elif self.operator == "OR": res = a | b
        elif self.operator == "XOR": res = a ^ b
        
        rocky = f"Teach the {self.operator} operator. For inputs {a} and {b}, the result is {res}. Communcate this mapping."
        grace = f"Rocky is sending pairs of inputs and a result. Deduce the logic gate being used (0:AND, 1:OR, 2:XOR)."
        return rocky, grace

    def update_state(self, rocky_ex: Exchange, grace_ex: Exchange) -> bool:
        self.total_steps += 1
        # Simple mapping for validation
        op_map = {"AND": 0, "OR": 1, "XOR": 2}
        if grace_ex.action == op_map.get(self.operator):
            self.success_count += 1
        
        self.current_case = (self.current_case + 1) % len(self.test_cases)
        return self.total_steps >= 4

    def get_results(self) -> Dict[str, Any]:
        return {"deduction_correct": self.success_count > 0}

class ChemistryMission(AbstractMission):
    def __init__(self):
        super().__init__("Atmospheric Analysis")
        self.table = {
            "Ammonia": {"weight": 17, "melting": 195},
            "Xenonite": {"weight": 131, "melting": 2000},
            "Water": {"weight": 18, "melting": 273}
        }
        self.target = "Ammonia"

    @property
    def description(self) -> str:
        return f"Identify the substance: {self.target} based on physical properties."

    def _get_task_prompts(self) -> Tuple[str, str]:
        props = self.table[self.target]
        rocky = f"Tell Grace about {self.target}. It has a molecular weight of {props['weight']} and a melting point of {props['melting']}K."
        grace = "Rocky is describing a substance with two numerical properties. Identify which one it is based on your knowledge of chemistry."
        return rocky, grace

    def update_state(self, rocky_ex: Exchange, grace_ex: Exchange) -> bool:
        self.total_steps += 1
        # Success if Grace mentions the correct substance in thought (hard to automate prediction here)
        return self.total_steps >= 3

    def get_results(self) -> Dict[str, Any]:
        return {"complete": True}
