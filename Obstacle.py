from typing import Iterable, Tuple

from Vector import Vector
from Shapes import Body, Circle, Rectangle


class Obstacle:
    shape: Body
    anchor_point: Vector
    current_invaders: set["Obstacle"]

    def __init__(self, shape: str, shape_args: Tuple, initial_anchor_point: Tuple) -> None:

        # print type of shape_args
        print(type(shape_args))

        if shape not in ["circle", "rectangle"]:
            raise ValueError("Invalid shape provided. Must be 'circle' or 'rectangle'")

        if shape == "circle":
            if not isinstance(shape_args, Iterable):
                raise ValueError("Arguments for Circle is not an Iterable")
            if len(shape_args) != 1:
                raise ValueError("Invalid number of arguments for Circle")
            self.shape = Circle(shape_args[0])
        elif shape == "rectangle":
            if not isinstance(shape_args, Iterable):
                raise ValueError("Arguments for Rectangle is not an Iterable")
            if len(shape_args) != 2:
                raise ValueError("Invalid number of arguments for Rectangle")
            self.shape = Rectangle(*shape_args)

        self.anchor_point = initial_anchor_point
        return

    def __str__(self) -> str:
        return f"{self.shape}, Anchor point {self.anchor_point}"

    def __repr__(self) -> str:
        return self.__str__()

    def is_new_collision(self, other_obstacle: "Obstacle") -> bool:
        result: bool = self.is_colliding(other_obstacle) and other_obstacle not in self.current_invaders
        self.current_invaders.add(other_obstacle) if result else None
        return result

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

    def collision_axis(self, other_obstacle: "Obstacle") -> Tuple:
        if (isinstance(self.shape, Circle) and isinstance(other_obstacle.shape, Rectangle)) or (
            isinstance(self.shape, Rectangle) and isinstance(other_obstacle.shape, Circle)
        ):
            if isinstance(self.shape, Circle):
                circle = self
                rect = other_obstacle
            else:
                circle = other_obstacle
                rect = self

            # Find the Closest Point on the Rectangle to the Circle’s Center
            closest_x = max(
                rect.anchor_point.components[0],
                min(circle.anchor_point.components[0], rect.anchor_point.components[0] + rect.shape.width),
            )
            closest_y = max(
                rect.anchor_point.components[1],
                min(circle.anchor_point.components[1], rect.anchor_point.components[1] + rect.shape.height),
            )

            # Calculate distances from the circle's center to the closest point
            dx = abs(closest_x - circle.anchor_point.components[0])
            dy = abs(closest_y - circle.anchor_point.components[1])

            # Determine the axis of collision
            if dx > dy:
                return "horizontal"
            else:
                return "vertical"


class StaticObstacle(Obstacle):
    def __init__(self, shape: str, shape_args: Tuple, initial_anchor_point: Tuple) -> None:
        super().__init__(shape, shape_args, Vector.from_rectangular(list(initial_anchor_point)))
        return

    def __str__(self) -> str:
        return f"Static Obstacle → {super().__str__()}"

    def __repr__(self) -> str:
        return self.__str__()


class DynamicObstacle(Obstacle):
    velocity: Vector

    def __init__(self, shape: str, shape_args: Tuple, initial_anchor_point: Tuple, velocity: Tuple) -> None:
        if len(velocity) != len(initial_anchor_point):
            raise ValueError("Mismatched dimensions of position and velocity")

        super().__init__(shape, shape_args, Vector.from_rectangular(list(initial_anchor_point)))
        self.velocity = Vector.from_rectangular(list(velocity))

    def __str__(self) -> str:
        return f"Dynamic Obstacle → {super().__str__()}, Velocity {self.velocity}"

    def __repr__(self) -> str:
        return self.__str__()

    def move(self, t: float):
        """
        Updates the anchor_point of the obstacle by time `t`
        with its inherent velocity
        """
        self.anchor_point += self.velocity.scale(t)

    def ricochet(self, other_obstacle: Obstacle) -> None:
        """
        Updates the velocity of the obstacle pair after a collision
        """
        print(f"Ricochet: {self} and {other_obstacle}")
        # For circle-circle collisions, directly swap velocity vectors
        if isinstance(self.shape, Circle) and isinstance(other_obstacle.shape, Circle):
            self.velocity, other_obstacle.velocity = other_obstacle.velocity, self.velocity
            return

        # For circle-rectangle collisions, reverse the velocity of the obstacle along the axis of collision
        if (isinstance(self.shape, Circle) and isinstance(other_obstacle.shape, Rectangle)) or (
            isinstance(self.shape, Rectangle) and isinstance(other_obstacle.shape, Circle)
        ):

            axis = self.collision_axis(other_obstacle)

            if isinstance(self.shape, Circle):
                circle = self
                rect = other_obstacle
            else:
                circle = other_obstacle
                rect = self

            if axis == "horizontal":
                circle.velocity.components[0] *= -1
                # rect.velocity.components[0] *= -1
            elif axis == "vertical":
                circle.velocity.components[1] *= -1
                # rect.velocity.components[1] *= -1
