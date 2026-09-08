"""Run and report a basic vertical rocket flight."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1] / "src"))

from rocket_sim import Rocket, apogee, simulate


rocket = Rocket(
    dry_mass=600,
    propellant_mass=400,
    thrust=20000,
    burn_time=10,
    drag_coefficient=0.5,
    reference_area=1.0,
)

result = simulate(rocket, simulation_time=300)

print("Simulation complete.")
print(f"Apogee: {apogee(result):.2f} m")
print(f"Max velocity: {result.y[1].max():.2f} m/s")
print(f"Final altitude: {result.y[0, -1]:.2f} m")
print(f"Final velocity: {result.y[1, -1]:.2f} m/s")
