from typing import Tuple
from numpy import sqrt
from obstacle import Obstacle
from shapes import Rectangle
from vector import Vector


class Node:
    position: Vector
    cost: float
    parent: "Node | None"

    def __init__(
        self, position: Tuple[float, float], /, parent: "Node | None" = None, cost: float = float("inf")
    ) -> None:
        self.position = Vector.from_rectangular(list(position))
        self.cost = cost
        self.parent = parent
        return

    def is_colliding(self, other: Obstacle) -> bool:
        # TODO: implement this for shapes other than rectangles
        if isinstance(other.shape, Rectangle):
            # Check for overlap
            return not (
                # node is to the right of the rectangle's right edge
                self.position.components[0]
                >= other.anchor_point.components[0] + other.shape.width
                # node is to the left of the rectangle's left edge
                or self.position.components[0] <= other.anchor_point.components[0]
                # node is below the rectangle's bottom edge
                or self.position.components[1]
                >= other.anchor_point.components[1] + other.shape.height
                # node is above the rectangle's top edge
                or self.position.components[1] <= other.anchor_point.components[1]
            )
        else:
            raise NotImplementedError("Collision detection for shapes other than rectangles is not implemented")

    def distance(self, other: "Node") -> float:
        return (self.position - other.position).get_magnitude()

    def __str__(self) -> str:
        return f"Node({self.position}, cost={self.cost}, parent={self.parent})"

    def __repr__(self) -> str:
        return self.__str__()
