from map_environment import MapEnvironment
from rrt import RRT
from rrt_star import RRT_Star
from map_layouts import layout_simple_cross, layout_maze, layout_urban

if __name__ == "__main__":
    env = MapEnvironment(layout=layout_maze())
    # env.preview_layout()

    ## RRT
    # rrt = RRT(env)
    # final_node, path = rrt.find_path()
    # env.visualize_path(rrt.nodes, path)

    ## RRT*
    rrt_star = RRT_Star(env)
    final_node, path = rrt_star.find_path()
    env.visualize_path(rrt_star.nodes, path)
