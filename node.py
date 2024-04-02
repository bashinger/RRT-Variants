from typing import Tuple
from numpy import sqrt
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

    def distance(self, other: "Node") -> float:
        return (self.position - other.position).get_magnitude()

    def __str__(self) -> str:
        return f"Node({self.position}, cost={self.cost}, parent={self.parent})"

    def __repr__(self) -> str:
        return self.__str__()
