class Crew:
    def __init__(self, config):
        self.size = config['crew_size']

    def consume(self, stores):
        stores['calories'].remove(2800 * self.size)
        stores['CO2'].add(1000 * self.size / 24)
