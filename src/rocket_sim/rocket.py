"""Rocket properties and simple constant-thrust mass model."""


class Rocket:
    """A vertically launched rocket with constant thrust during burn."""

    def __init__(
        self,
        dry_mass,
        propellant_mass,
        thrust,
        burn_time,
        drag_coefficient,
        reference_area,
    ):
        if dry_mass <= 0 or propellant_mass < 0:
            raise ValueError("Masses must be positive and non-negative.")
        if burn_time <= 0:
            raise ValueError("Burn time must be positive.")

        self.dry_mass = float(dry_mass)
        self.propellant_mass = float(propellant_mass)
        self.initial_mass = self.dry_mass + self.propellant_mass
        self.thrust = float(thrust)
        self.burn_time = float(burn_time)
        self.drag_coefficient = float(drag_coefficient)
        self.reference_area = float(reference_area)

    def mass(self, time):
        """Return rocket mass in kilograms at ``time`` in seconds."""
        if time <= self.burn_time:
            propellant_rate = self.propellant_mass / self.burn_time
            return self.initial_mass - propellant_rate * max(0.0, time)
        return self.dry_mass

    def thrust_at(self, time):
        """Return engine thrust in newtons at ``time`` in seconds."""
        if 0.0 <= time <= self.burn_time:
            return self.thrust
        return 0.0
