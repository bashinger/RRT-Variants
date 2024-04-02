from typing import Tuple
from Obstacle import DynamicObstacle, StaticObstacle


class Layout:
    size: Tuple[int, int]
    static_obstacles: list[StaticObstacle]
    start: Tuple[int, int]
    # TODO: Change end to goal
    end: Tuple[int, int]

    def __init__(self) -> None:
        # defaults
        self.size = (500, 500)
        self.start = (20, 20)
        self.end = (480, 480)


class DynamicLayout(Layout):
    dynamic_obstacles: list[DynamicObstacle]

    def update(self, t: float):
        """
        Update the positions of all dynamic obstacles over time `t`
        """
        [obstacle.move(t) for obstacle in self.dynamic_obstacles]
