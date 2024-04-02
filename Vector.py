from typing import Type, Tuple, List

from numpy import cos, sin, arctan2, sqrt, pi


class Vector:
    components: List[float]
    """
    Components of the vector.
    Up to 2 spatial and n miscellaneous.
    Spatial components are at the beginning of the list.
    """

    magnitude: float
    angle: float
    """
    Direction of the vector in radians.
    """

    def __init__(self, components: List[float] | None = None, polar: Tuple[float, float] | None = None) -> None:
        """
        Spatial components (up to 2) must be at the beginning of the list.
        A 1D vector will be assumed to have only an 'X' component
        """

        if (components is None and polar is None) or (components is not None and polar is not None):
            raise ValueError("Either components or polar coordinates must be provided")
        elif components is not None:
            self.components = components
            n_components = len(components)
            if n_components == 1:
                self.angle = 0
                self.magnitude = components[0]
                self.components[1] = 0
            elif n_components >= 2:
                # don't update the polar members until we need them
                self.__update_from_components()
                pass
        elif polar is not None:
            self.magnitude, self.angle = polar
            self.angle = self.angle % (2 * pi)  # pull angles back into the 0-2pi range
            self.components = [0, 0]
            self.__update_from_polar()

        return

    def __str__(self) -> str:
        return f"Vector → (î,ĵ) = ({self.components[0]}, {self.components[1]}), r = {self.magnitude}, θ = {self.angle}"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_polar(cls, r: float, theta: float) -> "Vector":
        """
        Constructs a vector from polar coordinates (theta in radians)
        """
        return cls(polar=(r, theta))

    @classmethod
    def from_rectangular(cls, components: List[float]) -> "Vector":
        """
        Constructs a vector from rectangular coordinates
        """
        return cls(components=components)

    def __update_from_components(self) -> None:
        if len(self.components) == 1:
            self.magnitude = self.components[0]
        else:
            self.magnitude = sqrt((self.components[0]) ** 2 + (self.components[1]) ** 2)
            # Divide by zero check
            self.angle = arctan2(self.components[1], self.components[0])
        return

    def __update_from_polar(self) -> None:
        if self.angle == 0:
            self.components[0] = self.magnitude
        else:
            self.components[0] = cos(self.angle) * self.magnitude
            self.components[1] = sin(self.angle) * self.magnitude
        return

    def scale(self, factor: float) -> "Vector":
        """
        Scale the vector by the given factor
        """
        self.__update_from_components()
        # hoping that numpy's trig can deal with -ve radians
        angle = (self.angle + pi) if factor < 0 else self.angle
        magnitude = abs(factor) * self.magnitude
        return Vector.from_polar(magnitude, angle)

    def __add__(self, other):
        if len(self.components) != len(other.components):
            raise ValueError("Cannot add vectors of different dimensions")
        return Vector.from_rectangular(
            [(self.components[i] + other.components[i]) for i in range(len(self.components))]
        )

    def __sub__(self, other):
        if len(self.components) != len(other.components):
            raise ValueError("Cannot subtract vectors of different dimensions")
        return Vector.from_rectangular(
            [(self.components[i] - other.components[i]) for i in range(len(self.components))]
        )
