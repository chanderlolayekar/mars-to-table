class FoodProcessor:
    def __init__(self, config):
        self.config = config
        self.calories_per_unit = config.get("calories_per_unit", 1000.0)
        self.max_daily_conversion = config.get("max_daily_conversion", 1.0)

    def tick(self, stores):
        edible = stores["edible_mycelium"].level
        if edible <= 0:
            return

        consumed = min(edible, self.max_daily_conversion)
        stores["edible_mycelium"].remove(consumed)
        stores["calories"].add(consumed * self.calories_per_unit)
