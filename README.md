# Rocket Trajectory Simulator

A small Python simulator for a vertically launched rocket. It models changing
rocket mass, constant thrust during the burn, atmospheric density, aerodynamic
drag, and the resulting altitude and velocity using SciPy's numerical ODE
solver.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the examples from the project root:

```powershell
python examples/test_atmosphere.py
python examples/basic_flight.py
```

Run the tests with:

```powershell
python -m pytest
```

## Physics

The vertical equations of motion are:

$$
\frac{dh}{dt}=v, \qquad
\frac{dv}{dt}=\frac{T-D}{m}-g
$$

with signed drag:

$$
D=\frac{1}{2}\rho C_D A v|v|
$$

The atmosphere is a simplified lapse-rate model. It is suitable for this
first milestone, but not for flight certification or high-altitude work.

## Project layout

- `src/rocket_sim/`: reusable simulation modules
- `examples/`: runnable demonstrations
- `tests/`: focused physics checks
- `results/`: generated output files

## Roadmap

Future versions can add variable gravity, a realistic thrust curve, specific
impulse and mass flow, two-dimensional flight, wind, Mach-dependent drag,
staging, and Monte Carlo uncertainty analysis.

