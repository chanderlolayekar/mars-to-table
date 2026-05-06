class BiomassProduction:
    def __init__(self, config):
        self.config = config

    def tick(self, stores):
        stores['inedible_biomass'].add(50)
