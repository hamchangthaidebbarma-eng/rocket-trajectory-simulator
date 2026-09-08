"""Plots for trajectory results."""

import matplotlib.pyplot as plt
import numpy as np


def plot_trajectory(result, show=True):
    """Plot altitude, velocity, and acceleration against time."""
    time = result.t
    altitude, velocity = result.y
    acceleration = np.gradient(velocity, time)

    figure, axes = plt.subplots(3, 1, sharex=True, figsize=(9, 8))
    axes[0].plot(time, altitude)
    axes[0].set_ylabel("Altitude [m]")
    axes[1].plot(time, velocity)
    axes[1].set_ylabel("Velocity [m/s]")
    axes[2].plot(time, acceleration)
    axes[2].set_ylabel("Acceleration [m/s²]")
    axes[2].set_xlabel("Time [s]")
    figure.tight_layout()

    if show:
        plt.show()
    return figure, axes
