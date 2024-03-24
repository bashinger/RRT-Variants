import numpy as np
import random
from map_environment import MapEnvironment
from rrt import RRT


class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Node Position (x coordinate, y coordinate)
        self.parent = parent  # Reference to the parent node


class DT_RRT_Star:
    def __init__(self, map_env: MapEnvironment, step_size=5, neighbor_radius=20):
        self.map_env = map_env
        self.step_size = step_size
        self.neighbor_radius = neighbor_radius
        self.nodes = [Node(map_env.start)]
        self.nodes[0].cost = 0

        self.sigma_r = 20  # Standard deviation for the radial distance
        self.mu_r = 2  # Mean radial distance
        self.sigma_theta = np.pi / 6  # Standard deviation for the angle in radians
        self.mu_theta = np.pi / 2  # Mean angle (e.g., pointing upwards)

    def sample_around(self, nodes):
        new_nodes = []
        random_node = random.choice(nodes)
        for _ in range(1000):
            r = np.random.normal(self.mu_r, self.sigma_r)
            theta = np.random.normal(self.mu_theta, self.sigma_theta)

            # Convert polar coordinates (r, theta) to Cartesian coordinates (dx, dy)
            dx = r * np.cos(theta)
            dy = r * np.sin(theta)

            # Create a new position by adding the offset to the current position
            new_position = (random_node[0] + dx, random_node[1] + dy)

            # Create a new node with the new position and add it to the list
            new_nodes.append(new_position)

        return (random_node, new_nodes)

    def random_gaussian_point(self, nodes):
        random_node = random.choice(nodes)
        r = np.random.normal(self.mu_r, self.sigma_r)
        theta = np.random.normal(self.mu_theta, self.sigma_theta)

        # Convert polar coordinates (r, theta) to Cartesian coordinates (dx, dy)
        dx = r * np.cos(theta)
        dy = r * np.sin(theta)

        # Create a new position by adding the offset to the current position
        gaussian_point = (random_node[0] + dx, random_node[1] + dy)

        return gaussian_point

    def distance(self, a, b):
        return np.linalg.norm(np.array(a) - np.array(b))

    def nearest_node(self, position):
        return min(self.nodes, key=lambda node: self.distance(node.position, position))

    def step_from_to(self, n1, n2):
        if self.distance(n1, n2) < self.step_size:
            return n2
        else:
            theta = np.arctan2(n2[1] - n1[1], n2[0] - n1[0])
            return n1[0] + self.step_size * np.cos(theta), n1[1] + self.step_size * np.sin(theta)

    def find_neighbors(self, new_node):
        return [node for node in self.nodes if self.distance(node.position, new_node.position) < self.neighbor_radius]

    def is_collision_free(self, node):
        for obstacle, size in self.map_env.obstacles:
            if (
                obstacle[0] <= node.position[0] <= obstacle[0] + size[0]
                and obstacle[1] <= node.position[1] <= obstacle[1] + size[1]
            ):
                return False
        return True

    def is_path_collision_free(self, start_pos, end_pos):
        steps = int(np.ceil(self.distance(start_pos, end_pos) / self.step_size))
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

    def choose_best_parent(self, new_node, neighbors):
        for neighbor in neighbors:
            potential_cost = neighbor.cost + self.distance(neighbor.position, new_node.position)
            if self.is_path_collision_free(neighbor.position, new_node.position) and potential_cost < new_node.cost:
                new_node.parent = neighbor
                new_node.cost = potential_cost

    def re_search_parent(self, new_node):
        # Initialize the potential parent as the node’s parent
        potential_parent = new_node.parent
        best_cost = new_node.cost
        found_better_parent = False

        # Traverse back up the tree towards the root
        current_node = new_node.parent
        while current_node is not None:
            # Calculate the potential cost if current_node were the parent
            if self.is_path_collision_free(current_node.position, new_node.position):
                potential_cost = current_node.cost + self.distance(current_node.position, new_node.position)

                # Check if this new potential parent offers a better (lower) cost
                if potential_cost < best_cost:
                    best_cost = potential_cost
                    potential_parent = current_node
                    found_better_parent = True

            # Move up the tree
            current_node = current_node.parent

        # If a better parent was found, update the parent and cost of new_node
        if found_better_parent:
            new_node.parent = potential_parent
            new_node.cost = best_cost

    def find_path(self):
        rrt = RRT(self.map_env)
        final_node, path = rrt.find_path()

        while True:
            random_position = self.random_gaussian_point(path)
            nearest = self.nearest_node(random_position)
            new_position = self.step_from_to(nearest.position, random_position)
            new_node = Node(new_position, nearest)
            new_node.cost = nearest.cost + self.distance(new_node.position, nearest.position)

            if self.is_collision_free(new_node):
                neighbors = self.find_neighbors(new_node)
                self.choose_best_parent(new_node, neighbors)
                self.re_search_parent(new_node)
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
