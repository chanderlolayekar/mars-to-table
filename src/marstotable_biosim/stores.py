from dataclasses import dataclass

@dataclass
class Store:
    name: str
    capacity: float
    level: float = 0.0

    def add(self, amount: float):
        self.level = min(self.capacity, self.level + amount)

    def remove(self, amount: float):
        self.level = max(0.0, self.level - amount)
