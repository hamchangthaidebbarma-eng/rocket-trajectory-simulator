import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from rocket_sim import Rocket, apogee, simulate
from rocket_sim.aerodynamics import drag_force
from rocket_sim.atmosphere import atmosphere


def test_atmosphere_decreases_with_altitude():
    sea_level = atmosphere(0)
    high_altitude = atmosphere(10_000)
    assert high_altitude[0] < sea_level[0]
    assert high_altitude[1] < sea_level[1]
    assert high_altitude[2] < sea_level[2]


def test_rocket_mass_reaches_dry_mass_after_burn():
    rocket = Rocket(600, 400, 20_000, 10, 0.5, 1.0)
    assert rocket.mass(0) == 1000
    assert rocket.mass(5) == 800
    assert rocket.mass(11) == 600
    assert rocket.thrust_at(11) == 0


def test_drag_opposes_motion():
    assert drag_force(100, 1.2, 0.5, 1.0) > 0
    assert drag_force(-100, 1.2, 0.5, 1.0) < 0


def test_simulation_produces_positive_apogee():
    rocket = Rocket(600, 400, 20_000, 10, 0.5, 1.0)
    result = simulate(rocket, simulation_time=30)
    assert result.success
    assert np.all(np.isfinite(result.y))
    assert apogee(result) > 0
    assert result.y[0, -1] >= 0
