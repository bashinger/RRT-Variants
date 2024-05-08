from visualiser import Visualiser
from map_layouts import layout_simple_cross, layout_maze, layout_narrow_pass, layout_narrow_pass_2, layout_space
from rrt import RRT
from rrt_star import RRT_Star
from dt_rrt_star import DT_RRT_Star
from q_rrt_star import Q_RRT_Star
from lazy_dt_rrt_star import Lazy_DT_RRT_Star
import time
import math

env = Visualiser(layout_space())
planner = Lazy_DT_RRT_Star(env)
final_node, path = planner.find_path()

env.visualize_path(planner.nodes, path)


def total_dist(path):
    ret = 0
    for i in range(len(path)-1):
        ret += math.sqrt((path[i][0] - path[i+1][0]) ** 2 + (path[i][1] - path[i+1][1]) ** 2)
    return ret

# layout_simple_cross(), layout_maze(), layout_narrow_pass(), layout_narrow_pass_2(), layout_space()
layouts = [layout_space()]

vars = [RRT, RRT_Star, Q_RRT_Star, DT_RRT_Star, Lazy_DT_RRT_Star]

n_samples = 10

with open("res.txt", "wt") as fd:
    for layout in layouts:
        for var in vars:
            fd.write(var.__name__ + " " + layout["name"] + "\n")
            planner = var(map_env=Visualiser(layout))
            for i in range(n_samples):
                print(var.__name__ + " " + layout["name"] + f"({i+1}/{n_samples})")
                ta = time.time_ns()
                _, path = planner.find_path()
                tb = time.time_ns()
                delta = (tb - ta) / 1e9
                fd.write(str(delta) + " " + str(total_dist(path)) + "\n")
            fd.write("\n")
            print()
