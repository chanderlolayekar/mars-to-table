class FoodProcessor:
    def __init__(self, config):
        self.config = config

    def tick(self, stores):
        if stores['edible_mycelium'].level > 5:
            stores['calories'].add(2500)
            stores['edible_mycelium'].remove(5)
