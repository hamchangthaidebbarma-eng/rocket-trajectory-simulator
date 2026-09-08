"""A simplified International Standard Atmosphere model."""

R = 287.05
G0 = 9.80665
L = 0.0065
T0 = 288.15
P0 = 101325.0


def atmosphere(altitude):
    """Return temperature, pressure, and density at ``altitude`` in metres."""
    altitude = max(0.0, float(altitude))
    temperature = max(T0 - L * altitude, 1.0)
    pressure = P0 * (temperature / T0) ** (G0 / (R * L))
    density = pressure / (R * temperature)
    return temperature, pressure, density
