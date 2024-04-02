"""
Geometric shapes that can be used as obstacles.
N.B.:
    - Must closely follow `matplotlib.patches` API.
    - Must have all of, and only the attributes of corresponding `matplotlib.patches`.
"""


class Body:
    def get_attrs(self) -> list:
        return [value for value in self.__dict__.values() if not callable(value)]


class Circle(Body):
    radius: float

    def __init__(self, radius: float) -> None:
        super().__init__()
        self.radius = radius

    def __str__(self) -> str:
        return f"Circle(r={self.radius})"

    def __repr__(self) -> str:
        return self.__str__()


class Rectangle(Body):
    width: float
    height: float

    def __init__(self, width: float, height: float) -> None:
        super().__init__()
        self.width = width
        self.height = height
        return

    def __str__(self) -> str:
        return f"Rectangle(w={self.width}),h={self.height}"

    def __repr__(self) -> str:
        return self.__str__()
