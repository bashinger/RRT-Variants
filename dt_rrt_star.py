import numpy as np
import random
from vector import Vector
from visualiser import Visualiser
from rrt import RRT
from debug import debug_planner, proc_time
from node import Node
from map import Map
from copy import deepcopy


class DT_RRT_Star(RRT):

    seed_path: list[Node]

    def __init__(self, map: Map, step_size: int = 5, neighbor_radius = 20, rrt_path: list[Node] | None = None):
        super().__init__(map, step_size)
        self.neighbor_radius = neighbor_radius
        self.sigma_r = 20  # Standard deviation for the radial distance
        self.mu_r = 2  # Mean radial distance
        self.sigma_theta = np.pi / 6  # Standard deviation for the angle in radians
        self.mu_theta = np.pi / 2  # Mean angle (e.g., pointing upwards)
        if rrt_path is not None:
            _, self.seed_path = self._shortcut_path(rrt_path[-1])
        else:
            rrt = super().find_path()
            _, self.seed_path = self._shortcut_path(self.map.path[-1])

        self.map.nodes = [self.map.start]
        self.map.path = None
        self.map.is_stagnant = False
        return


    @classmethod
    def from_rrt(cls, rrt: RRT, neighbor_radius=20):
        if (rrt.map.path == None):
            rrt.find_path()
        return cls(rrt.map, rrt.step_size, neighbor_radius, rrt.map.path)

    def random_gaussian_point(self, nodes: list[Node]) -> Vector:
        random_node = random.choice(nodes)
        r = np.random.normal(self.mu_r, self.sigma_r)
        theta = np.random.normal(self.mu_theta, self.sigma_theta)

        # Convert polar coordinates (r, theta) to Cartesian coordinates (dx, dy)
        # dx = r * np.cos(theta)
        # dy = r * np.sin(theta)
        ds = Vector.from_polar(r, theta)

        # Create a new position by adding the offset to the current position
        gaussian_point = random_node.position + ds
        # print(f"Sampled Gaussian point: {gaussian_point}")
        return gaussian_point

    def find_neighbors(self, new_node):
        return [node for node in self.map.nodes if node.distance(new_node) < self.neighbor_radius]

    def is_path_collision_free(self, node_from: Node, node_to: Node):
        diff = node_to.position - node_from.position
        dist = diff.magnitude
        steps = int(np.ceil(dist / self.step_size))
        ds = diff.scale(1 / float(steps))

        for step in range(1, steps + 1):
            intermediate_point = Node(tuple((node_from.position + ds.scale(step)).components[:2]))
            if self.map.is_colliding(intermediate_point):
                return False
        return True  # Path is collision-free

    def choose_best_parent(self, new_node: Node, neighbors: list[Node]):
        for neighbor in neighbors:
            potential_cost = neighbor.cost + neighbor.distance(new_node)
            if self.is_path_collision_free(neighbor, new_node) and potential_cost < new_node.cost:
                new_node.parent = neighbor
                new_node.cost = potential_cost

    def re_search_parent(self, new_node: Node):
        # Initialize the potential parent as the node’s parent
        potential_parent = new_node.parent
        best_cost = new_node.cost
        found_better_parent = False

        # Traverse back up the tree towards the root
        current_node = new_node.parent
        while current_node is not None:
            # Calculate the potential cost if current_node were the parent
            if self.is_path_collision_free(current_node, new_node):
                potential_cost = current_node.cost + current_node.distance(new_node)

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
        # first, notify any pauser daemons that we are starting
        # self.find_path.pause_condition.acquire(blocking=True)
        # rrt = RRT(self.map)
        # last_node, _ = rrt.find_path()
        # _, shortcut_path = self._shortcut_path(self.shortcut_path[-1])
        # print("INFO: found shortcut path!")
        # self.find_path.pause_condition.notify()
        # self.find_path.pause_condition.release()

        goal_reached = False
        while not goal_reached:
            # self.find_path.pause_condition.acquire(blocking=True)
            # self.find_path.pause_condition.wait_for(lambda: not self.find_path.paused)
            random_position = Node(tuple(self.random_gaussian_point(self.seed_path).components[:2]))
            nearest = self.map.nearest_node(random_position)
            new_position = self.step_from_to(nearest, random_position)
            new_node = Node(new_position, nearest)
            new_node.cost = nearest.cost + new_node.distance(nearest)

            if not self.map.is_colliding(new_node):
                neighbors = self.find_neighbors(new_node)
                self.choose_best_parent(new_node, neighbors)
                self.re_search_parent(new_node)
                self.map.nodes.append(new_node)

                if new_node.distance(self.map.end) <= self.step_size:
                    self.map.end.parent = new_node
                    self.map.path = self.map.invert(new_node)
                    print("INFO: Goal reached!")
                    goal_reached = True

            # self.find_path.pause_condition.release()
        return

    def iterate(self) -> None:
        random_position = Node(tuple(self.random_gaussian_point(self.seed_path).components[:2]))
        nearest = self.map.nearest_node(random_position)
        new_position = self.step_from_to(nearest, random_position)
        new_node = Node(new_position, nearest)
        new_node.cost = nearest.cost + new_node.distance(nearest)

        if not self.map.is_colliding(new_node):
            neighbors = self.find_neighbors(new_node)
            self.choose_best_parent(new_node, neighbors)
            self.re_search_parent(new_node)
            self.map.nodes.append(new_node)

            if new_node.distance(self.map.end) <= self.step_size:
                self.map.end.parent = new_node
                self.map.path = self.map.invert(new_node)
                print("INFO: Goal reached!")
        return

    @proc_time
    def _shortcut_path(self, last_final_node: Node):
        """
        Runs the `re_search_parent` operation on an existing path
        from the start point to the goal. Iterates from the goal, backwards,
        tracing `.parent` pointers to find the best parent for each node.

        N.B.:Additionally, it adds intermediate nodes to the path to aid in
        Gaussian sampling later on.

        Parameters:
        -----------
        final_node : Node
            Goal node with parent set, all the way back to the start node

        Returns:
        --------
        (Node, list[tuple])
            A tuple containing the last node in the path (excluding the goal)
            and the optimised path from the start to the goal
        """

        # for the first iteration, we start at the goal
        final_node = current_node = deepcopy(self.map.end)
        final_node.parent = last_final_node
        current_node.cost = last_final_node.cost + last_final_node.distance(self.map.end)
        self.re_search_parent(current_node)
        current_node = current_node.parent

        # iterate back up the tree to find the best parent for each node
        while current_node is not None:
            self.re_search_parent(current_node)
            current_node = current_node.parent

        # make the path have nodes each of increment `step_size`
        # by adding intermediate nodes. Needed for the Gaussian sampling
        # to work correctly
        current_node = final_node
        while current_node.parent is not None:
            if current_node.distance(current_node.parent) > self.step_size:
                new_position = self.step_from_to(current_node, current_node.parent)
                new_node = Node(new_position, parent=current_node.parent)
                new_node.cost = current_node.parent.cost + new_node.distance(current_node.parent)
                current_node.parent = new_node
            current_node = current_node.parent

        # retrace the path from the start to the goal
        # and return the optimised path
        #
        # TODO: change this to match the terminology the rest of the project
        # `final_node` needs to be a node *within step_size* of the goal
        # currently, it is the end goal node itself
        return final_node, self.map.invert(final_node)
