from visualiser import Visualiser
from map_layouts import layout_simple_cross, layout_maze, layout_urban
from rrt import RRT
from rrt_star import RRT_Star
from dt_rrt_star import DT_RRT_Star
from q_rrt_star import Q_RRT_Star
from lazy_dt_rrt_star import Lazy_DT_RRT_Star

if __name__ == "__main__":
    env = Visualiser(layout=layout_maze())
    # env.preview_layout()

    # Choose the RRT Variant to use
    # variant = RRT(env)
    # variant = RRT_Star(env)
    # variant = Q_RRT_Star(env)
    # variant = DT_RRT_Star(env)
    variant = Lazy_DT_RRT_Star(env)

    final_node, path = variant.find_path()
    env.visualize_path(variant.nodes, path)
