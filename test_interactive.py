from map_environment import MapEnvironment
from map_layouts import layout_simple_cross, layout_maze, layout_urban
from rrt import RRT
from rrt_star import RRT_Star
from dt_rrt_star import DT_RRT_Star
from lazy_dt_rrt_star import LazyDTRRTStar

from time import time_ns

def benchmark_old(planner):
    # time the `find_path` method
    start = time_ns()
    last_generated_node, path = planner.find_path()
    end = time_ns()
    return last_generated_node, path, (end - start) / 1e6

# def benchmark_new(planner):
#     # time the `find_path_zoomzoom` method
#     start = time_ns()
#     last_generated_node, path = planner.find_path_zoomzoom()
#     end = time_ns()
#     return last_generated_node, path, (end - start) / 1e6


if __name__ == "__main__":
    gondor = MapEnvironment(layout=layout_maze())
    rohan = MapEnvironment(layout=layout_simple_cross())
