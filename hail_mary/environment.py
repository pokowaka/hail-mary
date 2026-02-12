from typing import List

class PetrovaTask:
    """The shared objective: identifying patterns in the Astrophage-affected Sun."""
    def __init__(self, phenomenon: str = "primes"):
        self.phenomenon = phenomenon
        self.sequence = self._generate_data(phenomenon)

    def _generate_data(self, phenomenon: str) -> List[int]:
        if phenomenon == "primes":
            return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        elif phenomenon == "squares":
            return [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        elif phenomenon == "astrophage_growth":
            # Powers of 2
            return [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        else:
            raise ValueError(f"Unknown phenomenon: {phenomenon}")

    def get_data_points(self) -> List[int]:
        return self.sequence

    def verify_prediction(self, prediction: int, target_index: int) -> bool:
        if target_index >= len(self.sequence):
            return False
        return prediction == self.sequence[target_index]
