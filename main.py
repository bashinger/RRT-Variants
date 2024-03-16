from map_environment import MapEnvironment
from map_layouts import layout_simple_cross, layout_maze, layout_urban
from rrt import RRT
from rrt_star import RRT_Star
from dt_rrt_star import DT_RRT_Star

if __name__ == "__main__":
    env = MapEnvironment(layout=layout_maze())
    # env.preview_layout()

    ## RRT
    # rrt = RRT(env)
    # final_node, path = rrt.find_path()
    # env.visualize_path(rrt.nodes, path)

    ## RRT*
    # rrt_star = RRT_Star(env)
    # final_node, path = rrt_star.find_path()
    # env.visualize_path(rrt_star.nodes, path)

    # DT-RRT*
    dt_rrt_star = DT_RRT_Star(env)
    final_node, path = dt_rrt_star.find_path()
    env.visualize_path(dt_rrt_star.nodes, path)
