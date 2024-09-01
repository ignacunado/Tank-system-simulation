from settings import Settings
import numpy as np
from scipy.optimize import fsolve

settings = Settings()
g = settings.g
rho = settings.rho
delta_t = settings.delta_t

class Tank():
    "A class to create any cilyndrical vertical tank of the simulation"
    def __init__(self, high, diameter, liquid_high, nozzle_high,
                 nozzle_diameter, base_high, p1, p2):
        self.high = high # m
        self.diameter = diameter # m
        self.liquid_high = liquid_high # m
        self.nozzle_high = nozzle_high # m
        self.nozzle_diameter = nozzle_diameter # m
        self.base_high = base_high # m
        self.p1 = p1 # pa
        self.p2 = p2 # pa
        self.v2 = 0 # m/s
        self.q_inlet = 0 # m3/s

        self.tk_area = np.pi * (diameter**2)/4
        self.nozzle_area = np.pi * (nozzle_diameter**2)/4

    def tk_bem(self):
        self.v2 = np.sqrt((2 * (self.p1 - self.p2)/rho + 
                      2*g * (self.liquid_high - self.nozzle_high))/
                      (1 - self.nozzle_area / self.tk_area))

    def tk_update(self):
        if self.liquid_high > self.nozzle_high:
            self.liquid_high -= (self.v2/self.tk_area) * self.nozzle_area * delta_t
        if self.liquid_high <= self.nozzle_high:
            self.liquid_high = self.nozzle_high
            self.v2 = 0

    def tk_fill(self):
        self.liquid_high += (self.q_inlet/self.tk_area) * delta_t
