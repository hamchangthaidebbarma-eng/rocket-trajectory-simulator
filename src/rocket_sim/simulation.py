"""Numerical integration of the vertical rocket equations of motion."""

import numpy as np
from scipy.integrate import solve_ivp

from .aerodynamics import drag_force
from .atmosphere import atmosphere

G = 9.80665


def simulate(rocket, simulation_time=300.0, max_step=0.05):
    """Integrate altitude and velocity from a stationary launch at sea level."""
    if simulation_time <= 0:
        raise ValueError("Simulation time must be positive.")

    def equations(time, state):
        altitude, velocity = state
        mass = rocket.mass(time)
        thrust = rocket.thrust_at(time)
        _, _, density = atmosphere(altitude)
        drag = drag_force(
            velocity,
            density,
            rocket.drag_coefficient,
            rocket.reference_area,
        )
        acceleration = (thrust - drag) / mass - G
        return [velocity, acceleration]

    def ground_impact(time, state):
        if time < 1e-9:
            return 1.0
        return state[0]

    ground_impact.terminal = True
    ground_impact.direction = -1

    return solve_ivp(
        equations,
        (0.0, simulation_time),
        [0.0, 0.0],
        max_step=max_step,
        dense_output=True,
        events=ground_impact,
    )


def apogee(result):
    """Return the maximum altitude in metres from a solver result."""
    return float(np.max(result.y[0]))
