"""Print atmospheric conditions at representative altitudes."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1] / "src"))

from rocket_sim.atmosphere import atmosphere


for altitude in [0, 1000, 5000, 10000]:
    temperature, pressure, density = atmosphere(altitude)
    print(f"Altitude: {altitude:5.0f} m")
    print(f"Temperature: {temperature:.2f} K")
    print(f"Pressure: {pressure:.0f} Pa")
    print(f"Density: {density:.4f} kg/m^3")
    print()
