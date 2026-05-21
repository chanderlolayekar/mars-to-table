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
            'calories': Store('calories', 1e7, 1e6),
            'inedible_biomass': Store('inedible_biomass', 5000, 500),
            'edible_mycelium': Store('edible_mycelium', 1000, 50),
            'nutrients_N': Store('nutrients_N', 2000, 500),
            'CO2': Store('CO2', 5e4, 2000),
            'O2': Store('O2', 5e4, 15000),
            'water_potable': Store('water_potable', 20000, 15000),
            'water_grey': Store('water_grey', 5000, 100),
        }
        self.crew = Crew(config)
        self.plants = BiomassProduction(config)
        self.algae = AlgaeBioreactor(config)
        self.mycelium = MyceliumModule(config)
        self.insects = InsectModule(config)
        self.food_processor = FoodProcessor(config)
        self.water_rec = WaterRecovery(0.965)  # 96.5% matching Slide 3
        self.log = []

    def tick(self):
        # Adjust crew behavior slightly to feed greywater store
        self.crew.consume(self.stores)
        # Manually route crew wastewater output to greywater tank for recovery processing
        self.stores['water_grey'].add(self.crew.water_per_person_per_hour * self.crew.size * 0.9)
        
        self.plants.tick(self.stores)
        self.algae.tick(self.stores)
        self.mycelium.tick(self.stores)
        self.insects.tick(self.stores)
        self.food_processor.tick(self.stores)
        self.water_rec.tick(self.stores)
        
        self.log.append(self.get_state())
        self.time += 1

    def run(self, hours: int = 168):
        for _ in range(hours):
            self.tick()
        return pd.DataFrame(self.log)

    def get_state(self):
        return {name: s.level for name, s in self.stores.items()} | {'time': self.time}
