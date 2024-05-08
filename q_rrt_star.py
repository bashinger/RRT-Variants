import numpy as np
import math
from visualiser import Visualiser


class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Node Position (x coordinate, y coordinate)
        self.parent = parent  # Reference to the parent node
        self.cost = float("inf")  # Cost to reach this node


class Q_RRT_Star:
    def __init__(self, map_env: Visualiser, step_size=5, neighbor_radius=20):
        self.map_env = map_env
        self.step_size = step_size
        self.neighbor_radius = neighbor_radius
        self.nodes = [Node(map_env.start)]
        self.nodes[0].cost = 0

    def distance(self, a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def is_collision_free(self, node):
        for obstacle, size in self.map_env.obstacles:
            if (
                obstacle[0] <= node.position[0] <= obstacle[0] + size[0]
                and obstacle[1] <= node.position[1] <= obstacle[1] + size[1]
            ):
                return False
        return True

    def is_path_collision_free(self, start_pos, end_pos):
        steps = int(self.distance(start_pos, end_pos) / self.step_size) + 1
        dx = (end_pos[0] - start_pos[0]) / steps
        dy = (end_pos[1] - start_pos[1]) / steps

        for step in range(1, steps + 1):
            intermediate_point = (start_pos[0] + dx * step, start_pos[1] + dy * step)
            for obstacle, size in self.map_env.obstacles:
                # Check if intermediate_point is inside the current obstacle
                if (
                    obstacle[0] <= intermediate_point[0] <= obstacle[0] + size[0]
                    and obstacle[1] <= intermediate_point[1] <= obstacle[1] + size[1]
                ):
                    return False  # Path is not collision-free
        return True  # Path is collision-free

    def nearest_node(self, position):
        return min(self.nodes, key=lambda node: self.distance(node.position, position))

    def step_from_to(self, n1, n2):
        if self.distance(n1, n2) < self.step_size:
            return n2
        else:
            if n1[0] == n2[0]:
                if n1[1] < n2[1]:
                    return n1[0], n1[1] + self.step_size
                elif n1[1] > n2[1]:
                    return n1[0], n1[1] - self.step_size
                else:
                    return n1[0] + self.step_size, n1[1]
            x = (n2[1] - n1[1]) / (n2[0] - n1[0])
            if n2[0] < n1[0]:
                sign = -1
            else:
                sign = 1
            tmp = 1 / math.sqrt(1+x**2) * sign
            return n1[0] + self.step_size * (tmp), n1[1] + self.step_size * (x*tmp)

    def find_neighbors(self, new_node):
        return [node for node in self.nodes if self.distance(node.position, new_node.position) < self.neighbor_radius]

    def get_ancestors(self, node, all_nodes):
        current_node = node.parent
        while current_node is not None and current_node not in all_nodes:
            all_nodes.add(current_node)
            current_node = current_node.parent
        return all_nodes

    def choose_best_parent(self, new_node, neighbors):
        for neighbor in neighbors:
            potential_cost = neighbor.cost + self.distance(neighbor.position, new_node.position)
            if self.is_path_collision_free(neighbor.position, new_node.position) and potential_cost < new_node.cost:
                new_node.parent = neighbor
                new_node.cost = potential_cost

    def rewire(self, new_node, neighbors):
        nodes_to_rewire = set(neighbors)

        for neighbor in neighbors:
            self.get_ancestors(neighbor, nodes_to_rewire)

        for node_to_rewire in nodes_to_rewire:
            potential_cost = new_node.cost + self.distance(new_node.position, node_to_rewire.position)
            if (
                self.is_path_collision_free(new_node.position, node_to_rewire.position)
                and potential_cost < node_to_rewire.cost
            ):
                node_to_rewire.parent = new_node
                node_to_rewire.cost = potential_cost

    def find_path(self):
        while True:
            random_position = (np.random.randint(0, self.map_env.size[0]), np.random.randint(0, self.map_env.size[1]))
            nearest = self.nearest_node(random_position)
            new_position = self.step_from_to(nearest.position, random_position)
            new_node = Node(new_position, nearest)
            new_node.cost = nearest.cost + self.distance(new_node.position, nearest.position)

            if self.is_collision_free(new_node):
                neighbors = self.find_neighbors(new_node)
                self.choose_best_parent(new_node, neighbors)
                self.rewire(new_node, neighbors)
                self.nodes.append(new_node)

                if self.distance(new_node.position, self.map_env.goal) <= self.step_size:
                    return new_node, self._trace_path(new_node)

    def _trace_path(self, final_node):
        path = []
        current_node = final_node
        while current_node is not None:
            path.append(current_node.position)
            current_node = current_node.parent
        path.reverse()
        return path
