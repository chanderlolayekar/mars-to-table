class WaterRecovery:
    def __init__(self, efficiency=0.965):
        self.efficiency = efficiency

    def tick(self, stores):
        # Fallback creation of dirty water store if missing from basic template
        if 'water_grey' not in stores:
            return
            
        greywater_available = stores['water_grey'].level
        if greywater_available > 0:
            reclaimed_water = greywater_available * self.efficiency
            brine_waste = greywater_available * (1.0 - self.efficiency)
            
            stores['water_grey'].remove(greywater_available)
            stores['water_potable'].add(reclaimed_water)
            # Brine contains minerals redirected to hydroponic nutrient tanks
            stores['nutrients_N'].add(brine_waste * 0.05)
