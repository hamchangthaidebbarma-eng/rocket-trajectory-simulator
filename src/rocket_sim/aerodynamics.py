"""Aerodynamic forces for the trajectory model."""


def drag_force(velocity, density, drag_coefficient, reference_area):
    """Return signed drag force in newtons, opposing the velocity."""
    return (
        0.5
        * density
        * drag_coefficient
        * reference_area
        * velocity
        * abs(velocity)
    )
