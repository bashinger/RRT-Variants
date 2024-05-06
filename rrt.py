# Future Scope:
# 1. Use Deque to sure nodes in the path in the function _trace_path


from threading import Thread
from time import sleep
from typing import Tuple
import numpy as np
from map import Map
from node import Node


class RRT:
    """
    An implementation of the original *Rapidly-exploring Random Tree*
    algorithm (Steven M. LaValle, 1998).
    """

    map: Map
    step_size: int

    def __init__(self, map: Map, step_size=10) -> None:
        self.map = map
        self.step_size = step_size  # Maximum distance to extend the tree in each iteration

    def step_from_to(self, n1: Node, n2: Node) -> Tuple[float, float]:
        diff = n2.position - n1.position
        dist = diff.magnitude
        if dist < self.step_size:
            return tuple(n2.position.components[:2])
        else:
            diff = diff.scale(float(self.step_size) / dist)
            # print("step_from_to magnitude returned: ", diff.magnitude)
            return tuple((n1.position + diff).components[:2])

    def find_path(self):
        while True:
            random_node = Node(
                (
                    np.random.randint(0, self.map.size[0]),
                    np.random.randint(0, self.map.size[1]),
                )
            )
            nearest = self.map.nearest_node(random_node)
            new_position = self.step_from_to(nearest, random_node)
            new_node = Node(new_position, parent=nearest)
            # print(new_node)

            if not self.map.is_colliding(new_node):
                new_node.cost = nearest.cost + nearest.distance(new_node)
                self.map.nodes.append(new_node)
                if new_node.distance(self.map.end) <= self.step_size:
                    self.map.end.parent = new_node
                    self.map.path = self.map.invert(new_node)
                    return


    def seek_new_candidate(self):
        random_node = Node(
            (
                np.random.randint(0, self.map.size[0]),
                np.random.randint(0, self.map.size[1]),
            )
        )
        nearest = self.map.nearest_node(random_node)
        new_position = self.step_from_to(nearest, random_node)
        new_node = Node(new_position, parent=nearest)
        # print(new_node)

        if not self.map.is_colliding(new_node):
            new_node.cost = nearest.cost + nearest.distance(new_node)
            self.map.nodes.append(new_node)
            if new_node.distance(self.map.end) <= self.step_size:
                self.map.end.parent = new_node
                self.map.path = self.map.invert(new_node)
                return True
        return False
