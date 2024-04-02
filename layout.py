from typing import Tuple
from obstacle import DynamicObstacle, StaticObstacle
import shapes


class Layout:
    size: Tuple[int, int]
    start: Tuple[int, int]
    # TODO: Change end to goal
    end: Tuple[int, int]
    static_obstacles: list[StaticObstacle]
    dynamic_obstacles: list[DynamicObstacle]

    def __init__(
        self,
        size: Tuple[int, int] = (500, 500),
        start: Tuple[int, int] = (20, 20),
        end: Tuple[int, int] = (480, 480),
        static_obstacles: list[StaticObstacle] = [],
        dynamic_obstacles: list[DynamicObstacle] = [],
    ) -> None:
        # defaults
        self.size = size
        self.start = start
        self.end = end
        self.static_obstacles = [
            StaticObstacle((0, 0), shapes.Rectangle, (1, 500)),  # Map's Left border
            StaticObstacle((0, 499), shapes.Rectangle, (500, 1)),  # Map's Top border
            StaticObstacle((499, 0), shapes.Rectangle, (1, 500)),  # Map's Right border
            StaticObstacle((0, 0), shapes.Rectangle, (500, 1)),  # Map's Bottom border
            *static_obstacles,
        ]
        self.dynamic_obstacles = dynamic_obstacles
        return
