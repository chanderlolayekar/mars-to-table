import math

class AlgaeBioreactor:
    def __init__(self, config):
        self.config = config
        # Biokinetic constants for Spirulina platensis
        self.X = 0.5  # Initial biomass density (g/L)
        self.X_max = 4.0  # Saturation density
        self.mu_max = 0.08  # Max growth rate per hour
        self.I0 = 120.0  # Incident light intensity (PAR photons)
        self.kappa = 0.15  # Light extinction coefficient (L / g * cm)
        self.L = 5.0  # Tube path length diameter (cm)

    def calculate_avg_light(self, I0, X, kappa, L):
        """Beer-Lambert law integration over the PBR tube cross-section."""
        if kappa * X * L == 0:
            return I0
        return (I0 / (kappa * X * L)) * (1 - math.exp(-kappa * X * L))

    def tick(self, stores):
        dt = 1 / 24.0  # Hourly resolution
        
        # Calculate growth based on light availability inside the modular racks
        I_avg = self.calculate_avg_light(self.I0, self.X, self.kappa, self.L)
        f_light = I_avg / (40.0 + I_avg)  # Monod kinetic scaling for light saturation
        
        dX = self.mu_max * self.X * (1 - self.X / self.X_max) * f_light * dt
        self.X += dX
        
        # Stoichiometric coefficients for photosynthesis:
        # 1 gram of Algae draws down approx 1.88g CO2 and generates 1.47g O2
        co2_required = dX * 1.88 * 15  # Scaled for array sizing
        o2_produced = dX * 1.47 * 15
        
        if stores['CO2'].level >= co2_required:
            stores['CO2'].remove(co2_required)
            stores['O2'].add(o2_produced)
            stores['inedible_biomass'].add(dX * 10)  # Harvested biomass output
