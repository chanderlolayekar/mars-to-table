class InsectModule:
    def __init__(self, config):
        self.L = 0.0
        self.mu_max = 0.20
        self.Y_LS = 0.28

    def tick(self, stores):
        dt = 1 / 24.0
        waste_available = stores['inedible_biomass'].level
        if waste_available > 10:
            f_W = waste_available / (20 + waste_available)
            dL = self.mu_max * self.L * (1 - self.L / 500) * f_W * dt
            self.L += dL
            stores['inedible_biomass'].remove(dL / self.Y_LS)
            stores['edible_mycelium'].add(dL * 0.4)
            stores['nutrients_N'].add(dL * 0.15)
