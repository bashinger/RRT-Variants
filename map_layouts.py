# Description: This file contains the layout of the maps for the path planning algorithms.
# The layout of the maps is defined as a function that returns the size of the map and the obstacles.

from typing import Type, Tuple, List
from time import time

from numpy import cos, sin, sqrt, tan


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
                pass
        elif polar is not None:
            self.magnitude, self.angle = polar
            self.components = [0, 0]
            self.__update_from_polar()

        return

    @classmethod
    def from_polar(cls, r: float, theta: float) -> Type["Vector"]:
        """
        Constructs a vector from polar coordinates (theta in radians)
        """
        return cls(polar=(r, theta))

    @classmethod
    def from_rectangular(cls, components: List[float]) -> Type["Vector"]:
        """
        Constructs a vector from rectangular coordinates
        """
        return cls(components=components)

    def __update_from_components(self) -> None:
        if len(self.components) == 1:
            self.magnitude = self.components[0]
        else:
            self.magnitude = sqrt((self.components[0]) ** 2 + (self.components[1]) ** 2)
            self.angle = tan(self.components[1] / self.components[0])
        return

    def __update_from_polar(self) -> None:
        if self.angle == 0:
            self.components[0] = self.magnitude
        else:
            self.components[0] = cos(self.angle) * self.magnitude
            self.components[1] = sin(self.angle) * self.magnitude
        return

    def scale(self, factor: float) -> Type["Vector"]:
        """
        Scale the vector by the given factor
        """
        self.__update_from_components()
        # hoping that numpy's trig can deal with -ve radians
        angle = self.angle * -1 if factor < 0 else self.angle
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


class Body:
    pass


class Circle(Body):
    radius: float

    def __init__(self, radius: float) -> None:
        super().__init__()
        self.radius = radius

    def __str__(self) -> str:
        return f"Circle of radius {self.radius}"

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
        return f"Rectangle of width {self.width} and height {self.height}"

    def __repr__(self) -> str:
        return self.__str__()


class Obstacle:
    shape: Body
    anchor_point: Vector

    def __init__(self, shape: Body, initial_anchor_point: Tuple) -> None:
        self.shape = shape
        self.anchor_point = initial_anchor_point
        return

    def __str__(self) -> str:
        return f"Obstacle: {self.shape} at ({self.anchor_point.components[0]},{self.anchor_point.components[1]})"

    def __repr__(self) -> str:
        return self.__str__()

    def is_colliding(self, other_obstacle: "Obstacle") -> bool:
        if isinstance(self.shape, Circle) and isinstance(other_obstacle.shape, Circle):
            # Calculate distance between centers
            dx = self.anchor_point.components[0] - other_obstacle.anchor_point.components[0]
            dy = self.anchor_point.components[1] - other_obstacle.anchor_point.components[1]
            # TODO: optimize
            distance = (dx**2 + dy**2) ** 0.5
            return distance <= (self.shape.radius + other_obstacle.shape.radius)

        elif isinstance(self.shape, Rectangle) and isinstance(other_obstacle.shape, Rectangle):
            # Check for overlap
            return not (
                # self is to the right of other
                self.anchor_point.components[0]
                >= other_obstacle.anchor_point.components[0] + other_obstacle.shape.width
                # self is to the left of other
                or self.anchor_point.components[0] + self.shape.width <= other_obstacle.anchor_point.components[0]
                # self is below other
                or self.anchor_point.components[1]
                >= other_obstacle.anchor_point.components[1] + other_obstacle.shape.height
                # self is above other
                or self.anchor_point.components[1] + self.shape.height <= other_obstacle.anchor_point.components[1]
            )

        elif (isinstance(self.shape, Circle) and isinstance(other_obstacle.shape, Rectangle)) or (
            isinstance(self.shape, Rectangle) and isinstance(other_obstacle.shape, Circle)
        ):
            # Check for overlap
            if isinstance(self.shape, Circle):
                circle = self
                rect = other_obstacle
            else:
                circle = other_obstacle
                rect = self

            ## Try this method(Copilot's) later (Commented out for now)
            # # Find closest point on rectangle to circle
            # closest_x = max(rect.anchor_point[0], min(circle.anchor_point[0], rect.anchor_point[0] + rect.shape.width))
            # closest_y = max(rect.anchor_point[1], min(circle.anchor_point[1], rect.anchor_point[1] + rect.shape.height)

            # # Calculate distance between closest point and circle center
            # dx = circle.anchor_point[0] - closest_x
            # dy = circle.anchor_point[1] - closest_y
            # distance = (dx**2 + dy**2) ** 0.5
            # return distance <= circle.shape.radius

            ## Method inspired from https://stackoverflow.com/a/402010/13483425
            # Calculate absolute distance between the circle's center and the rectangle's center
            dx = abs(circle.anchor_point.components[0] - (rect.anchor_point.components[0] + rect.shape.width / 2))
            dy = abs(circle.anchor_point.components[1] - (rect.anchor_point.components[1] + rect.shape.height / 2))

            # Check if circle is too far from rectangle in either dimension for an intersection
            if dx > (rect.shape.width / 2 + circle.shape.radius):
                return False
            if dy > (rect.shape.height / 2 + circle.shape.radius):
                return False

            if dx <= (rect.shape.width / 2):
                return True
            if dy <= (rect.shape.height / 2):
                return True

            # Check for intersection with rectangle corner
            cornerDistance_sq = (dx - rect.shape.width / 2) ** 2 + (dy - rect.shape.height / 2) ** 2

            return cornerDistance_sq <= (circle.shape.radius**2)


class StaticObstacle(Obstacle):
    def __init__(self, shape: Body, initial_anchor_point: Tuple) -> None:
        super().__init__(shape, Vector.from_rectangular(list(initial_anchor_point)))
        return


class DynamicObstacle(Obstacle):
    velocity: Vector

    def __init__(self, shape: Body, initial_anchor_point: Tuple, velocity: Tuple) -> None:
        if len(velocity) != len(initial_anchor_point):
            raise ValueError("Mismatched dimensions of position and velocity")

        super().__init__(shape, Vector.from_rectangular(list(initial_anchor_point)))
        self.velocity = Vector.from_rectangular(list(velocity))

    def move(self, t: float):
        """
        Updates the anchor_point of the obstacle by time `t`
        with its inherent velocity
        """
        self.anchor_point += self.velocity.scale(t)

    def ricochet(self):
        """
        Updates the velocity of the obstacle after a collision
        """
        self.velocity = self.velocity.scale(-1)


class Layout:
    size: Tuple[int, int]
    obstacles: list
    start: Tuple[int, int]
    end: Tuple[int, int]

    def __init__(self) -> None:
        # defaults
        self.size = (500, 500)
        self.start = (20, 20)
        self.end = (480, 480)


class DynamicLayout(Layout):
    dynamic_obstacles: list[DynamicObstacle]

    def update(self, t: float):
        """
        Update the positions of all dynamic obstacles over time `t`
        """
        [obstacle.move(t) for obstacle in self.dynamic_obstacles]


## LAYOUTS


### DYNAMIC LAYOUTS
# Basic dynamic layout
# No static obstacles
class LayoutBalloons(DynamicLayout):
    def __init__(self) -> None:
        super().__init__()
        self.static_obstacles = [
            StaticObstacle(Rectangle(5, 495), (5, 5)),  # Map's Left border
            StaticObstacle(Rectangle(5, 495), (495, 5)),  # Map's Right border
            StaticObstacle(Rectangle(495, 5), (5, 495)),  # Map's Top border
            StaticObstacle(Rectangle(495, 5), (5, 5)),  # Map's Bottom border
        ]
        self.dynamic_obstacles = [
            DynamicObstacle(Circle(40), (30, 210), (40, -30)),
            DynamicObstacle(Circle(20), (70, 30), (24, 63)),
            DynamicObstacle(Circle(30), (100, 100), (321, 523)),
            DynamicObstacle(Circle(30), (200, 150), (325, 64)),
            DynamicObstacle(Circle(30), (350, 400), (235, -95)),
            DynamicObstacle(Circle(30), (100, 380), (241, 245)),
            DynamicObstacle(Circle(30), (170, 420), (853, -583)),
        ]
        return


### STATIC LAYOUTS
# The Cross - A simple cross-shaped environment
# Testing basic navigation
def layout_simple_cross():
    layout = {
        "size": (500, 500),
        "start": (10, 10),
        "end": (480, 480),
        "name": "cross",
        "obstacles": [
            ((225, 100), (50, 300)),  # Vertical bar
            ((100, 225), (300, 50)),  # Horizontal bar
        ],
    }
    return layout


# The Maze - A simple maze environment
# Testing basic pathfinding
def layout_maze():
    layout = {
        "size": (500, 500),
        "start": (250, 50),
        "goal": (50, 450),
        "name": "maze",
        "obstacles": [
            # Vertical segments
            ((200, 0), (10, 100)),
            ((400, 0), (10, 200)),
            ((100, 100), (10, 100)),
            ((300, 200), (10, 100)),
            ((200, 300), (10, 100)),
            ((400, 300), (10, 100)),
            # Horizontal segments
            ((200, 100), (100, 10)),
            ((100, 200), (310, 10)),
            ((0, 300), (200, 10)),
            ((100, 400), (310, 10)),
        ],
    }
    return layout


##### FIX THIS
# The Corridors - Environment with narrow corridors
# Testing pathfinding in constrained spaces
def layout_corridors():
    size = (500, 500)
    obstacles = [
        ((0, 100), (450, 50)),  # Horizontal top
        ((50, 350), (450, 50)),  # Horizontal bottom
        ((100, 0), (50, 200)),  # Vertical left
        ((350, 300), (50, 200)),  # Vertical right
        ((200, 200), (100, 100)),  # Central block
    ]
    return size, obstacles


##### FIX THIS
# The Spiral - Environment with a spiral of obstacles
# Tests ability to navigate through progressively tighter spaces.
def layout_spiral():
    size = (500, 500)
    obstacles = [
        ((0, 0), (460, 20)),  # Outer top
        ((0, 0), (20, 460)),  # Outer left
        ((480, 0), (20, 460)),  # Outer right
        ((0, 480), (460, 20)),  # Outer bottom
        ((40, 40), (380, 20)),  # Inner top
        ((40, 40), (20, 380)),  # Inner left
        ((400, 40), (20, 380)),  # Inner right
        ((40, 400), (380, 20)),  # Inner bottom
        ((80, 80), (300, 20)),  # More inner top
        ((80, 80), (20, 300)),  # More inner left
        ((320, 80), (20, 300)),  # More inner right
        ((80, 320), (300, 20)),  # More inner bottom
    ]
    return size, obstacles


##### FIX THIS
# The Urban - Urban environment with blocks and narrow passages,
# Ideal for testing advanced pathfinding in constrained spaces.
def layout_urban(size=(500, 500)):
    obstacles = [
        ((100, 100), (300, 50)),
        ((100, 150), (50, 200)),
        ((350, 150), (50, 200)),
        ((150, 350), (200, 50)),
        ((200, 200), (100, 50)),
        ((200, 250), (50, 100)),
    ]
    return size, obstacles


def layout_narrow_pass():
    layout = {
        "size": (500, 500),
        "start": (10, 10),
        "end": (480, 480),
        "name": "narrow_pass",
        "obstacles": [
            ((100, 0), (20, 490)),
            ((130, 10), (20, 500)),
            ((160, 0), (20, 245)),
            ((160, 255), (20, 500)),
        ],
    }
    return layout
