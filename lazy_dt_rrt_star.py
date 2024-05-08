import numpy as np
import random
from vector import Vector
from visualiser import Visualiser
from dt_rrt_star import DT_RRT_Star
from rrt import RRT
from debug import debug_planner, proc_time
from node import Node
from map import Map
from copy import deepcopy

class Lazy_DT_RRT_Star(DT_RRT_Star):
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
                self.map.nodes.append(new_node)

                if new_node.distance(self.map.end) <= self.step_size:
                    print("INFO: Goal reached!")
                    self.map.end.parent = new_node
                    self.map.path = self.map.invert(new_node)
                    goal_reached = True

            # self.find_path.pause_condition.release()

            # optimise path (re_search_parent)
        self.optimise_path()
        return

    def iterate(self) -> None:
        if self.map.path is None:
            return self.seek_new_candidate()
        else:
            return self.optimise_path()

    def seek_new_candidate(self) -> None:
        random_position = Node(tuple(self.random_gaussian_point(self.seed_path).components[:2]))
        nearest = self.map.nearest_node(random_position)
        new_position = self.step_from_to(nearest, random_position)
        new_node = Node(new_position, nearest)
        new_node.cost = nearest.cost + new_node.distance(nearest)

        if not self.map.is_colliding(new_node):
            neighbors = self.find_neighbors(new_node)
            self.choose_best_parent(new_node, neighbors)
            self.map.nodes.append(new_node)

            if new_node.distance(self.map.end) <= self.step_size:
                self.map.end.parent = new_node
                self.map.path = self.map.invert(new_node)
                # NOTE: not setting map as stagnant!
                print("INFO: Goal reached!")
        return

    def _trace_path(self, final_node):
        path: list[tuple] = []
        current_node = final_node
        while current_node is not None:
            path.append(current_node.position)
            current_node = current_node.parent
        path.reverse()
        return path

    def optimise_path(self):
        """
        Runs the `re_search_parent` operation on an existing path
        from the start point to the goal. Iterates from the goal, backwards,
        tracing `.parent` pointers to find the best parent for each node.

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

        if self.map.path is None:
            raise ValueError("Cannot optimise a nonexsitent path!")

        last_final_node = self.map.path[-1]
        # for the first iteration, we start at the goal
        final_node = current_node = self.map.end
        final_node.parent = last_final_node
        current_node.cost = last_final_node.cost + last_final_node.distance(self.map.end)
        self.re_search_parent(current_node)
        current_node = current_node.parent

        # iterate back up the tree to find the best parent for each node
        while current_node is not None:
            self.re_search_parent(current_node)
            current_node = current_node.parent

        self.map.path = self.map.invert(final_node)
        self.map.is_stagnant = True
        return
