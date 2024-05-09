from visualiser import DynamicVisualiser, Visualiser
from map_layouts import LayoutCross, LayoutMaze, LayoutBalloons
from map import Map
from rrt import RRT
from rrt_star import RRT_Star
from dt_rrt_star import DT_RRT_Star
from q_rrt_star import Q_RRT_Star
from lazy_dt_rrt_star import Lazy_DT_RRT_Star

if __name__ == "__main__":

    # CROSS LAYOUT
    # env = Map(LayoutCross())
    # planner = DT_RRT_Star(env)
    # planner = Lazy_DT_RRT_Star(env)

    # MAZE LAYOUT
    # env = Map(LayoutMaze())
    # planner = DT_RRT_Star(env)
    # planner = Lazy_DT_RRT_Star(env)

    # ALLEY LAYOUT
    # env = Map(LayoutAlley())
    # planner = DT_RRT_Star(env)
    # planner = Lazy_DT_RRT_Star(env)

    # SPACE LAYOUT
    # env = Map(LayoutSpace())
    # planner = DT_RRT_Star(env)
    # planner = Lazy_DT_RRT_Star(env)

    renderer = DynamicVisualiser(1, env, planner)
    # renderer = Visualiser(env)

    # Choose the RRT Variant to use
    # variant = RRT(env)
    # variant = RRT_Star(env)
    # variant = Q_RRT_Star(env)

    # (a)
    # base_planner = RRT(env)
    # planner = DT_RRT_Star.from_rrt(base_planner)
    # planner = Lazy_DT_RRT_Star.from_rrt(base_planner)

    # OR

    # (b)
    # base_planner = RRT(env)
    # base_planner.find_path()
    # reference_path = base_planner.map.path

    # # to view ref path
    # _ = Visualiser(env)

    # # planner = DT_RRT_Star(env, rrt_path=reference_path)
    # planner = Lazy_DT_RRT_Star(env, rrt_path=reference_path)
