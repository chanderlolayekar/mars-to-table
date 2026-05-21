import pandas as pd

from .stores import Store
from .crew import Crew
from .plants import BiomassProduction
from .algae import AlgaeBioreactor
from .mycelium import MyceliumModule
from .insects import InsectModule
from .food_processor import FoodProcessor
from .water_recovery import WaterRecovery

class Simulation:
    def __init__(self, config):
        self.time = 0
        self.crew_size = config.get('crew_size', 15)
        self.stores = {
            'calories': Store('calories', 1e6, 5e5),
            'inedible_biomass': Store('inedible_biomass', 1000, 200),
            'edible_mycelium': Store('edible_mycelium', 500, 0),
            'nutrients_N': Store('nutrients_N', 1000, 300),
            'CO2': Store('CO2', 1e4, 5000),
            'O2': Store('O2', 1e4, 8000),
            'water_potable': Store('water_potable', 5000, 4000),
        }
        self.crew = Crew(config)
        self.plants = BiomassProduction(config)
        self.algae = AlgaeBioreactor(config)
        self.mycelium = MyceliumModule(config)
        self.insects = InsectModule(config)
        self.food_processor = FoodProcessor(config)
        self.water_rec = WaterRecovery(0.95)
        self.log = []

    def tick(self):
        self.crew.consume(self.stores)
        self.plants.tick(self.stores)
        self.algae.tick(self.stores)
        self.mycelium.tick(self.stores)
        self.insects.tick(self.stores)
        self.food_processor.tick(self.stores)
        self.water_rec.tick(self.stores)
        print("calories=", self.stores["calories"].level, "edible_mycelium=", self.stores["edible_mycelium"].level)
        self.log.append(self.get_state())
        self.time += 1

    def run(self, hours: int = 43800):
        for _ in range(hours):
            self.tick()
        return pd.DataFrame(self.log)

    def get_state(self):
        return {name: s.level for name, s in self.stores.items()} | {'time': self.time}
