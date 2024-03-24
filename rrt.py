# Future Scope:
# 1. Use Deque to sure nodes in the path in the function _trace_path


import numpy as np
from map_environment import MapEnvironment


class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Node Position (x coordinate, y coordinate)
        self.parent = parent  # Reference to the parent node
        self.cost = float("inf")  # Cost to reach this node


class RRT:
    def __init__(self, map_env: MapEnvironment, step_size=10):
        self.map_env = map_env
        self.step_size = step_size  # Maximum distance to extend the tree in each iteration
        self.nodes = [Node(map_env.start)]
        self.nodes[0].cost = 0 # Cost to reach the start node is 0

    def distance(self, a, b):
        return np.linalg.norm(np.array(a) - np.array(b))

    def is_collision_free(self, node):
        for obstacle_anchor_point, size in self.map_env.obstacles:
            if (
                # Node's X coordinate is between the obstacle's left and right edges
                obstacle_anchor_point[0] <= node.position[0] <= obstacle_anchor_point[0] + size[0]
                # Node's Y coordinate is between the obstacle's top and bottom edges
                and obstacle_anchor_point[1] <= node.position[1] <= obstacle_anchor_point[1] + size[1]
            ):
                return False
        return True

    def nearest_node(self, n):
        return min(self.nodes, key=lambda node: self.distance(node.position, n.position))

    def step_from_to(self, n1, n2):
        if self.distance(n1, n2) < self.step_size:
            return n2
        else:
            # Theta is the angle between the two points according to the x-axis
            theta = np.arctan2(n2[1] - n1[1], n2[0] - n1[0])
            return n1[0] + self.step_size * np.cos(theta), n1[1] + self.step_size * np.sin(theta)

    def find_path(self):
        while True:
            random_node = Node(
                (
                    np.random.randint(0, self.map_env.size[0]),
                    np.random.randint(0, self.map_env.size[1]),
                )
            )
            nearest = self.nearest_node(random_node)
            new_position = self.step_from_to(nearest.position, random_node.position)
            new_node = Node(new_position, nearest)

            if self.is_collision_free(new_node):
                new_node.cost = nearest.cost + self.distance(nearest.position, new_node.position)
                self.nodes.append(new_node)
                if self.distance(new_node.position, self.map_env.goal) <= self.step_size:
                    return new_node, self._trace_path(new_node)

    def _trace_path(self, final_node):
        path = []
        current_node = final_node
        while current_node is not None:
            path.append(current_node.position)
            current_node = current_node.parent
        path.reverse()  # Reverse the path to start from the beginning
        return path
