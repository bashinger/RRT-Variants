from visualiser import DynamicVisualiser, Visualiser
from map_layouts import LayoutCross, LayoutMaze, LayoutBalloons
from map import Map
from rrt import RRT
from rrt_star import RRT_Star
from dt_rrt_star import DT_RRT_Star
from q_rrt_star import Q_RRT_Star
from lazy_dt_rrt_star import Lazy_DT_RRT_Star

if __name__ == "__main__":
    env = Map(LayoutCross())
    # env.preview_layout()

    # Choose the RRT Variant to use
    # variant = RRT(env)
    # variant = RRT_Star(env)
    # variant = Q_RRT_Star(env)
    # variant = DT_RRT_Star(env)
    # variant = Lazy_DT_RRT_Star(env)


    # base_planner = RRT(env)
    # planner = DT_RRT_Star.from_rrt(base_planner)
    # OR
    base_planner = RRT(env)
    base_planner.find_path()
    reference_path = base_planner.map.path
    planner = DT_RRT_Star(env, rrt_path=reference_path)
    _ = Visualiser(env)
    planner = DT_RRT_Star(env, rrt_path=reference_path)

    renderer = DynamicVisualiser(40, env, planner)
