"""Interactive frontend for the vertical rocket trajectory simulator.

Run with: ``streamlit run app.py``
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rocket_sim import Rocket, apogee, simulate
from rocket_sim.atmosphere import atmosphere


st.set_page_config(
    page_title="Rocket Trajectory Simulator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container { max-width: 1200px; padding-top: 2.5rem; }
        [data-testid="stMetric"] {
            background: #101827;
            border: 1px solid #24334a;
            border-radius: 0.75rem;
            padding: 1rem;
        }
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color: #f8fafc; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _density_at(altitudes: np.ndarray) -> np.ndarray:
    """Return atmospheric densities for an altitude array."""
    return np.array([atmosphere(altitude)[2] for altitude in altitudes])


def _build_rocket() -> tuple[Rocket, float]:
    """Collect validated simulation settings from the sidebar."""
    with st.sidebar:
        st.header("Vehicle configuration")
        st.caption("All quantities use SI units.")
        dry_mass = st.number_input("Dry mass [kg]", min_value=1.0, value=600.0, step=10.0)
        propellant_mass = st.number_input(
            "Propellant mass [kg]", min_value=0.0, value=400.0, step=10.0
        )
        thrust = st.number_input("Engine thrust [N]", min_value=0.0, value=20_000.0, step=500.0)
        burn_time = st.number_input("Burn time [s]", min_value=0.1, value=10.0, step=0.5)

        st.header("Aerodynamics")
        drag_coefficient = st.number_input(
            "Drag coefficient (Cd)", min_value=0.0, value=0.5, step=0.05
        )
        reference_area = st.number_input(
            "Reference area [m²]", min_value=0.01, value=1.0, step=0.1
        )

        st.header("Run settings")
        simulation_time = st.slider("Maximum simulation time [s]", 20, 600, 300, 10)
        st.caption("The run stops early if the rocket returns to the ground.")

    return (
        Rocket(
            dry_mass=dry_mass,
            propellant_mass=propellant_mass,
            thrust=thrust,
            burn_time=burn_time,
            drag_coefficient=drag_coefficient,
            reference_area=reference_area,
        ),
        float(simulation_time),
    )


st.title("🚀 Rocket Trajectory Simulator")
st.write("Explore a physics-based, vertical launch trajectory in real time.")

rocket, simulation_time = _build_rocket()

if rocket.thrust <= rocket.initial_mass * 9.80665:
    st.warning("Thrust is below the rocket's initial weight, so it will not lift off.")

result = simulate(rocket, simulation_time=simulation_time)
time = result.t
altitude, velocity = result.y
acceleration = np.gradient(velocity, time)
apogee_index = int(np.argmax(altitude))
densities = _density_at(altitude)
dynamic_pressure = 0.5 * densities * velocity**2

metric_columns = st.columns(4)
metric_columns[0].metric("Apogee", f"{apogee(result):,.1f} m")
metric_columns[1].metric("Time to apogee", f"{time[apogee_index]:.1f} s")
metric_columns[2].metric("Maximum velocity", f"{np.max(velocity):,.1f} m/s")
metric_columns[3].metric("Peak dynamic pressure", f"{np.max(dynamic_pressure) / 1000:,.1f} kPa")

trajectory_data = pd.DataFrame(
    {
        "Time [s]": time,
        "Altitude [m]": altitude,
        "Velocity [m/s]": velocity,
        "Acceleration [m/s²]": acceleration,
        "Dynamic pressure [kPa]": dynamic_pressure / 1000,
    }
)

charts_tab, data_tab, model_tab = st.tabs(["Trajectory", "Flight data", "Model"])

with charts_tab:
    st.subheader("Flight profile")
    left, right = st.columns(2)
    with left:
        st.caption("Altitude")
        st.line_chart(trajectory_data, x="Time [s]", y="Altitude [m]", color="#38bdf8")
        st.caption("Velocity")
        st.line_chart(trajectory_data, x="Time [s]", y="Velocity [m/s]", color="#a78bfa")
    with right:
        st.caption("Acceleration")
        st.line_chart(trajectory_data, x="Time [s]", y="Acceleration [m/s²]", color="#f59e0b")
        st.caption("Dynamic pressure")
        st.line_chart(
            trajectory_data, x="Time [s]", y="Dynamic pressure [kPa]", color="#34d399"
        )

with data_tab:
    st.subheader("Simulation samples")
    st.dataframe(trajectory_data.round(3), width="stretch", hide_index=True)
    st.download_button(
        "Download flight data as CSV",
        data=trajectory_data.to_csv(index=False),
        file_name="rocket_trajectory.csv",
        mime="text/csv",
    )

with model_tab:
    st.subheader("Vertical-flight model")
    st.latex(r"\frac{dh}{dt}=v \qquad \frac{dv}{dt}=\frac{T-D}{m}-g")
    st.latex(r"D=\frac{1}{2}\rho C_D A v|v|")
    st.write(
        "Mass decreases linearly while the engine burns. Atmospheric density uses a "
        "simplified ISA lapse-rate model, and signed drag opposes both ascent and descent."
    )
