class FoodProcessor:
    def __init__(self, config):
        self.config = config
        self.calories_per_mycelium = config.get("calories_per_mycelium", 500.0)

    def tick(self, stores):
        edible = stores["edible_mycelium"].level
        if edible >= 5:
            amount = 5
            stores["calories"].add(amount * self.calories_per_mycelium)
            stores["edible_mycelium"].remove(amount)
