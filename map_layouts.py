# Description: This file contains the layout of the maps for the path planning algorithms.
# The layout of the maps is defined as a function that returns the size of the map and the obstacles.

from Shapes import Circle, Rectangle
from Obstacle import DynamicObstacle, StaticObstacle
from Layout import DynamicLayout

## LAYOUTS


### DYNAMIC LAYOUTS
# Basic dynamic layout
# No static obstacles
class LayoutBalloons(DynamicLayout):
    def __init__(self) -> None:
        super().__init__()
        self.static_obstacles = [
            StaticObstacle(Rectangle(5, 490), (5, 5)),  # Map's Left border
            StaticObstacle(Rectangle(5, 495), (490, 5)),  # Map's Right border
            StaticObstacle(Rectangle(495, 5), (5, 490)),  # Map's Top border
            StaticObstacle(Rectangle(495, 5), (5, 5)),  # Map's Bottom border
        ]
        self.dynamic_obstacles = [
            DynamicObstacle(Circle(40), (60, 210), (600, -360)),
            DynamicObstacle(Circle(20), (70, 60), (300, -663)),
            DynamicObstacle(Circle(30), (100, 100), (721, 223)),
            DynamicObstacle(Circle(30), (200, 150), (125, 664)),
            DynamicObstacle(Circle(30), (350, 400), (935, -95)),
            DynamicObstacle(Circle(30), (100, 380), (1041, 145)),
            DynamicObstacle(Circle(30), (170, 420), (253, -883)),
        ]
        return


### STATIC LAYOUTS
# The Cross - A simple cross-shaped environment
# Testing basic navigation
def layout_simple_cross():
    layout = {
        "size": (500, 500),
        "start": (10, 10),
        "end": (480, 480),
        "name": "cross",
        "obstacles": [
            ((225, 100), (50, 300)),  # Vertical bar
            ((100, 225), (300, 50)),  # Horizontal bar
        ],
    }
    return layout


# The Maze - A simple maze environment
# Testing basic pathfinding
def layout_maze():
    layout = {
        "size": (500, 500),
        "start": (250, 50),
        "goal": (50, 450),
        "name": "maze",
        "obstacles": [
            # Vertical segments
            ((200, 0), (10, 100)),
            ((400, 0), (10, 200)),
            ((100, 100), (10, 100)),
            ((300, 200), (10, 100)),
            ((200, 300), (10, 100)),
            ((400, 300), (10, 100)),
            # Horizontal segments
            ((200, 100), (100, 10)),
            ((100, 200), (310, 10)),
            ((0, 300), (200, 10)),
            ((100, 400), (310, 10)),
        ],
    }
    return layout


##### FIX THIS
# The Corridors - Environment with narrow corridors
# Testing pathfinding in constrained spaces
def layout_corridors():
    size = (500, 500)
    obstacles = [
        ((0, 100), (450, 50)),  # Horizontal top
        ((50, 350), (450, 50)),  # Horizontal bottom
        ((100, 0), (50, 200)),  # Vertical left
        ((350, 300), (50, 200)),  # Vertical right
        ((200, 200), (100, 100)),  # Central block
    ]
    return size, obstacles


##### FIX THIS
# The Spiral - Environment with a spiral of obstacles
# Tests ability to navigate through progressively tighter spaces.
def layout_spiral():
    size = (500, 500)
    obstacles = [
        ((0, 0), (460, 20)),  # Outer top
        ((0, 0), (20, 460)),  # Outer left
        ((480, 0), (20, 460)),  # Outer right
        ((0, 480), (460, 20)),  # Outer bottom
        ((40, 40), (380, 20)),  # Inner top
        ((40, 40), (20, 380)),  # Inner left
        ((400, 40), (20, 380)),  # Inner right
        ((40, 400), (380, 20)),  # Inner bottom
        ((80, 80), (300, 20)),  # More inner top
        ((80, 80), (20, 300)),  # More inner left
        ((320, 80), (20, 300)),  # More inner right
        ((80, 320), (300, 20)),  # More inner bottom
    ]
    return size, obstacles


##### FIX THIS
# The Urban - Urban environment with blocks and narrow passages,
# Ideal for testing advanced pathfinding in constrained spaces.
def layout_urban(size=(500, 500)):
    obstacles = [
        ((100, 100), (300, 50)),
        ((100, 150), (50, 200)),
        ((350, 150), (50, 200)),
        ((150, 350), (200, 50)),
        ((200, 200), (100, 50)),
        ((200, 250), (50, 100)),
    ]
    return size, obstacles


def layout_narrow_pass():
    layout = {
        "size": (500, 500),
        "start": (10, 10),
        "end": (480, 480),
        "name": "narrow_pass",
        "obstacles": [
            ((100, 0), (20, 490)),
            ((130, 10), (20, 500)),
            ((160, 0), (20, 245)),
            ((160, 255), (20, 500)),
        ],
    }
    return layout
