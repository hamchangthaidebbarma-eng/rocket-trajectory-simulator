"""Core models for the vertical rocket trajectory simulator."""

from .rocket import Rocket
from .simulation import apogee, simulate

__all__ = ["Rocket", "apogee", "simulate"]
