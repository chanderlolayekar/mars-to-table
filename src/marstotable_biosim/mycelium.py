class MyceliumModule:
    def __init__(self, config):
        self.X = 0.0
        self.S = 500.0
        self.mu_max = 0.22
        self.X_max = 150.0
        self.Y_XS = 0.50
        self.Y_NX = 0.10
        self.fruiting_active = False
        self.fruiting_timer = 0

    def tick(self, stores):
        dt = 1 / 24.0
        if stores['inedible_biomass'].level > 10:
            f_S = stores['inedible_biomass'].level / (20 + stores['inedible_biomass'].level)
            dX = self.mu_max * self.X * (1 - self.X / self.X_max) * f_S * dt
            self.X += dX
            dS = (1 / self.Y_XS) * dX * 1000
            stores['inedible_biomass'].remove(dS)
            stores['edible_mycelium'].add(dX * 0.25)
            stores['nutrients_N'].add(self.Y_NX * dX * 10)
            stores['edible_mycelium'].add(dX * 0.75)

        if self.X >= 0.85 * self.X_max and not self.fruiting_active:
            self.fruiting_active = True
            self.fruiting_timer = 4
        elif self.fruiting_active:
            self.fruiting_timer -= dt
            if self.fruiting_timer <= 0:
                yield_fresh = 0.30 * self.X
                stores['edible_mycelium'].add(yield_fresh * 0.25)
                stores['edible_mycelium'].add(yield_fresh * 0.75)
                self.X = 0.2 * self.X_max
                self.fruiting_active = False
