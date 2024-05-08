"""
Tools to bring layouts to life and maintain updates to them
(from e.g. path planners like DT_RRT_Star)
"""

## Summary
# ---===---

## Imports
# ---===---
from typing import Type, List, Tuple
from layout import Layout
from node import Node
from copy import deepcopy

from obstacle import Obstacle

## Definitions
# ---===---


class Map(Layout):
    """
    A dynamic, self-updating layout with a list of nodes discovered by a path planner
    """

    type: Type[Layout]
    nodes: List[Node]
    path: List[Node] | None
    is_stagnant: bool

    def __init__(self, layout: Layout) -> None:
        # super().__init__(layout.size, layout.start.position, layout.end.position, layout.static_obstacles, layout.dynamic_obstacles)
        # self.nodes = [Node(layout.start.position, None, 0)]

        # ! this could be a bad practice!
        self.__dict__ = deepcopy(layout.__dict__)

        self.type = type(layout)
        self.nodes = [self.start]
        self.path = None
        self.is_stagnant = False
        return

    def __str__(self) -> str:
        return (
            f"Map of layout {self.type}:\n"
            f"Size: {self.size}\n"
            f"Start: {self.start.position}\n"
            f"End: {self.end.position}\n"
            f"Static Obstacles: {self.static_obstacles}\n"
            f"Dynamic Obstacles: {self.dynamic_obstacles}\n"
            f"Nodes: {self.nodes}"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def update(self, t: float) -> None:
        """
        Update the map with new nodes

        Parameters:
        ----------
        t: float
            The time interval the update will reflect
        """

        # update the dynamic obstacles
        obstacles: List[Obstacle] = [*self.static_obstacles, *self.dynamic_obstacles]
        for obstacle in self.dynamic_obstacles:
            obstacle.move(t)
            for other_obstacle in obstacles:
                if obstacle != other_obstacle and obstacle.is_new_collision(other_obstacle):
                    obstacle.ricochet(other_obstacle)
        return

    def is_colliding(self, node: Node) -> bool:
        """
        Check if a node is colliding with any *STATIC* obstacles
        """
        for obstacle in self.static_obstacles:
            if node.is_colliding(obstacle):
                return True
        return False

    def nearest_node(self, node: Node) -> Node:
        """
        Find the nearest existing node on the map to a given node
        """
        return min(self.nodes, key=lambda x: x.distance(node))

    def invert(self, final_node):
        """
        A function that recurses back up the tree of nodes, building a path to the final node
        """
        path = []
        current_node = final_node
        while current_node is not None:
            path.append(current_node)
            current_node = current_node.parent
        path.reverse()  # Reverse the path to start from the beginning
        return path
