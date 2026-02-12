import random
import logging

class CommChannel:
    def __init__(self, noise_level: float = 0.0, energy_per_bit: float = 1.0, total_energy: float = float('inf')):
        self.noise_level = noise_level
        self.energy_per_bit = energy_per_bit
        self.remaining_energy = total_energy
        self.energy_used = 0.0

    def transmit(self, chords: str) -> str:
        """Transmits signal, applying noise and deducting energy."""
        if not chords:
            return ""

        # Deduct energy for each '1' bit (or all bits, but let's say '1's represent a pulse)
        for bit in chords:
            cost = self.energy_per_bit if bit == '1' else 0.1 # even 0 has a small carrier cost
            if self.remaining_energy >= cost:
                self.remaining_energy -= cost
                self.energy_used += cost
            else:
                logging.warning("Out of energy! Signal truncated.")
                return "" # Signal dies

        # Apply noise
        output = []
        for bit in chords:
            if random.random() < self.noise_level:
                output.append('1' if bit == '0' else '0')
            else:
                output.append(bit)
        
        return "".join(output)

    def is_depleted(self) -> bool:
        return self.remaining_energy <= 0
