class Crew:
    def __init__(self, config):
        self.size = config.get('crew_size', 15)
        self.calories_per_person_per_hour = config.get('calories_per_person_per_hour', 175)
        self.co2_per_person_per_hour = config.get('co2_per_person_per_hour', 0.625)
        self.water_per_person_per_hour = config.get('water_per_person_per_hour', 0.1)
        self.waste_per_person_per_hour = config.get('waste_per_person_per_hour', 0.02)

    def consume(self, stores):
        stores['calories'].remove(self.calories_per_person_per_hour * self.size)
        stores['CO2'].add(self.co2_per_person_per_hour * self.size)
        stores['water_potable'].remove(self.water_per_person_per_hour * self.size)
        stores['inedible_biomass'].add(self.waste_per_person_per_hour * self.size)
