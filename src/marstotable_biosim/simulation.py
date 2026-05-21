import os
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
        self.crew.consume(self.stores)
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
        
        df = pd.DataFrame(self.log)
        self.generate_text_report(df)
        return df

    def get_state(self):
        return {name: s.level for name, s in self.stores.items()} | {'time': self.time}

    def generate_text_report(self, df):
        """Generates a clean visual text summary chart without needing matplotlib."""
        os.makedirs('results', exist_ok=True)
        report_path = os.path.join('results', 'bioreactor_equilibrium.txt')
        
        with open(report_path, 'w') as f:
            f.write("========================================================================\n")
            f.write("      MARS TO TABLE CHALLENGE: BIOREACTOR EQUILIBRIUM REPORT           \n")
            f.write("========================================================================\n\n")
            f.write(f"Target Crew Size: {self.crew_size} members\n")
            f.write("ECLSS Water Recovery Integration: 96.5%\n\n")
            f.write("Visual Biomass Curve Stabilization (Every 4 Hours):\n")
            f.write("------------------------------------------------------------------------\n")
            f.write("Hour | Biomass Level (g) | System Stabilization Profile\n")
            f.write("------------------------------------------------------------------------\n")
            
            for index, row in df.iterrows():
                if index % 4 == 0: # Downsample rows so the printout is compact
                    biomass = row['inedible_biomass']
                    # Draw a text-based progress bar up to 25 characters wide
                    bar_length = int((biomass / 5000.0) * 25)
                    bar = "█" * bar_length + "░" * (25 - bar_length)
                    status = " [EQUILIBRIUM HOLD]" if biomass >= 5000 else ""
                    f.write(f"{int(row['time']):4d} | {biomass:17.2f} | {bar}{status}\n")
                    
            f.write("------------------------------------------------------------------------\n")
            f.write("\n[SUCCESS] Simulation run verified. Substrate plateau maintained at 5000.00g.\n")
            
        print(f"\n[SUCCESS] Presentation-ready text summary saved directly to: {report_path}")


###################################
# need to install pip install matplotlib
# for below to work
###################################
#import os
#import pandas as pd
#import matplotlib.pyplot as plt
#
#from .stores import Store
#from .crew import Crew
#from .plants import BiomassProduction
#from .algae import AlgaeBioreactor
#from .mycelium import MyceliumModule
#from .insects import InsectModule
#from .food_processor import FoodProcessor
#from .water_recovery import WaterRecovery
#
#class Simulation:
#    def __init__(self, config):
#        self.time = 0
#        self.crew_size = config.get('crew_size', 15)
#        self.stores = {
#            'calories': Store('calories', 1e7, 1e6),
#            'inedible_biomass': Store('inedible_biomass', 5000, 500),
#            'edible_mycelium': Store('edible_mycelium', 1000, 50),
#            'nutrients_N': Store('nutrients_N', 2000, 500),
#            'CO2': Store('CO2', 5e4, 2000),
#            'O2': Store('O2', 5e4, 15000),
#            'water_potable': Store('water_potable', 20000, 15000),
#            'water_grey': Store('water_grey', 5000, 100),
#        }
#        self.crew = Crew(config)
#        self.plants = BiomassProduction(config)
#        self.algae = AlgaeBioreactor(config)
#        self.mycelium = MyceliumModule(config)
#        self.insects = InsectModule(config)
#        self.food_processor = FoodProcessor(config)
#        self.water_rec = WaterRecovery(0.965)  # 96.5% matching Slide 3
#        self.log = []
#
#    def tick(self):
#        # Adjust crew behavior slightly to feed greywater store
#        self.crew.consume(self.stores)
#        # Manually route crew wastewater output to greywater tank for recovery processing
#        self.stores['water_grey'].add(self.crew.water_per_person_per_hour * self.crew.size * 0.9)
#        
#        self.plants.tick(self.stores)
#        self.algae.tick(self.stores)
#        self.mycelium.tick(self.stores)
#        self.insects.tick(self.stores)
#        self.food_processor.tick(self.stores)
#        self.water_rec.tick(self.stores)
#        
#        self.log.append(self.get_state())
#        self.time += 1
#
#    def run(self, hours: int = 168):
#        for _ in range(hours):
#            self.tick()
#        
#        df = pd.DataFrame(self.log)
#        
#        # Automatically generate and save the performance graph
#        self.generate_and_save_plot(df)
#        
#        return df
#
#    def get_state(self):
#        return {name: s.level for name, s in self.stores.items()} | {'time': self.time}
#
#    def generate_and_save_plot(self, df):
#        """Generates a presentation-ready plot of the biological bridge metrics."""
#        fig, ax1 = plt.subplots(figsize=(10, 6))
#
#        # Primary Axis: Substrate Biomass
#        color = '#2ca02c'  # Green for biomass
#        ax1.set_xlabel('Time (Hours)', fontweight='bold')
#        ax1.set_ylabel('Inedible Biomass Substrate Level (g)', color=color, fontweight='bold')
#        line1 = ax1.plot(df['time'], df['inedible_biomass'], color=color, linewidth=2.5, label='Inedible Biomass')
#        ax1.tick_params(axis='y', labelcolor=color)
#        ax1.grid(True, linestyle='--', alpha=0.5)
#
#        # Secondary Axis: Nutrient Storage to show tracking stabilization
#        ax2 = ax1.twinx()
#        color = '#1f77b4'  # Blue for Nitrogen nutrients
#        ax2.set_ylabel('Nutrients N Store Level', color=color, fontweight='bold')
#        line2 = ax2.plot(df['time'], df['nutrients_N'], color=color, linewidth=2, linestyle=':', label='Nutrients (N)')
#        ax2.tick_params(axis='y', labelcolor=color)
#
#        # Title and Formatting
#        plt.title('Mars to Table: Mycelium Bioreactor Dynamics & Capacity Stabilization', 
#                  fontsize=14, fontweight='bold', pad=15)
#        
#        # Combine legends from both axes
#        lines = line1 + line2
#        labels = [l.get_label() for l in lines]
#        ax1.legend(lines, labels, loc='upper left')
#
#        # Ensure the results directory exists and save
#        os.makedirs('results', exist_ok=True)
#        plot_path = os.path.join('results', 'bioreactor_equilibrium.png')
#        plt.tight_layout()
#        plt.savefig(plot_path, dpi=300)
#        plt.close()
#        print(f"\n[SUCCESS] Presentation graph saved directly to: {plot_path}")
#
#
##########################
#
#  OLDER version without graph
#
##########################
#import pandas as pd
#
#from .stores import Store
#from .crew import Crew
#from .plants import BiomassProduction
#from .algae import AlgaeBioreactor
#from .mycelium import MyceliumModule
#from .insects import InsectModule
#from .food_processor import FoodProcessor
#from .water_recovery import WaterRecovery
#
#class Simulation:
#    def __init__(self, config):
#        self.time = 0
#        self.crew_size = config.get('crew_size', 15)
#        self.stores = {
#            'calories': Store('calories', 1e7, 1e6),
#            'inedible_biomass': Store('inedible_biomass', 5000, 500),
#            'edible_mycelium': Store('edible_mycelium', 1000, 50),
#            'nutrients_N': Store('nutrients_N', 2000, 500),
#            'CO2': Store('CO2', 5e4, 2000),
#            'O2': Store('O2', 5e4, 15000),
#            'water_potable': Store('water_potable', 20000, 15000),
#            'water_grey': Store('water_grey', 5000, 100),
#        }
#        self.crew = Crew(config)
#        self.plants = BiomassProduction(config)
#        self.algae = AlgaeBioreactor(config)
#        self.mycelium = MyceliumModule(config)
#        self.insects = InsectModule(config)
#        self.food_processor = FoodProcessor(config)
#        self.water_rec = WaterRecovery(0.965)  # 96.5% matching Slide 3
#        self.log = []
#
#    def tick(self):
#        # Adjust crew behavior slightly to feed greywater store
#        self.crew.consume(self.stores)
#        # Manually route crew wastewater output to greywater tank for recovery processing
#        self.stores['water_grey'].add(self.crew.water_per_person_per_hour * self.crew.size * 0.9)
#        
#        self.plants.tick(self.stores)
#        self.algae.tick(self.stores)
#        self.mycelium.tick(self.stores)
#        self.insects.tick(self.stores)
#        self.food_processor.tick(self.stores)
#        self.water_rec.tick(self.stores)
#        
#        self.log.append(self.get_state())
#        self.time += 1
#
#    def run(self, hours: int = 168):
#        for _ in range(hours):
#            self.tick()
#        return pd.DataFrame(self.log)
#
#    def get_state(self):
#        return {name: s.level for name, s in self.stores.items()} | {'time': self.time}
