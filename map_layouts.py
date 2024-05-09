# Description: This file contains the layout of the maps for the path planning algorithms.
# The layout of the maps is defined as a function that returns the size of the map and the obstacles.

from obstacle import DynamicObstacle, StaticObstacle
from layout import Layout
import shapes

## LAYOUTS


### DYNAMIC LAYOUTS
# Basic dynamic layout
# No static obstacles
class LayoutBalloons(Layout):
    def __init__(self) -> None:
        super().__init__()
        self.static_obstacles = [
            StaticObstacle((0, 0), shapes.Rectangle, (5, 500)),  # Map's Left border
            StaticObstacle((495, 0), shapes.Rectangle, (5, 500)),  # Map's Right border
            StaticObstacle((0, 495), shapes.Rectangle, (500, 5)),  # Map's Top border
            StaticObstacle((0, 0), shapes.Rectangle, (500, 5)),  # Map's Bottom border
        ]
        self.dynamic_obstacles = [
            DynamicObstacle((60, 210), (600, -360), shapes.Circle, (40,)),
            DynamicObstacle((70, 60), (300, -663), shapes.Circle, (20,)),
            DynamicObstacle((100, 100), (721, 223), shapes.Circle, (30,)),
            DynamicObstacle((170, 420), (253, -883), shapes.Circle, (30,)),
            DynamicObstacle((200, 150), (125, 664), shapes.Circle, (30,)),
            DynamicObstacle((350, 400), (935, -95), shapes.Circle, (30,)),
            DynamicObstacle((100, 380), (1041, 145), shapes.Circle, (30,)),
        ]
        return


### STATIC LAYOUTS
# The Cross - A simple cross-shaped environment
class LayoutCross(Layout):
    def __init__(self) -> None:
        super().__init__()
        self.static_obstacles = [
            StaticObstacle((225, 100), shapes.Rectangle, (50, 300)),  # Vertical bar
            StaticObstacle((100, 225), shapes.Rectangle, (300, 50)),  # Horizontal bar
        ]
        return


# Maze
class LayoutMaze(Layout):
    def __init__(self) -> None:
        super().__init__(start=(250, 50), end=(50, 450))
        self.static_obstacles = [
            # # Vertical segments
            # StaticObstacle((200, 0), shapes.Rectangle, (10, 100)),
            # StaticObstacle((400, 0), shapes.Rectangle, (10, 200)),
            # StaticObstacle((100, 100), shapes.Rectangle, (10, 100)),
            # StaticObstacle((300, 200), shapes.Rectangle, (10, 100)),
            # # Horizontal segments
            # StaticObstacle((0, 200), shapes.Rectangle, (100, 10)),
            # StaticObstacle((100, 300), shapes.Rectangle, (200, 10)),
            # StaticObstacle((300, 100), shapes.Rectangle, (100, 10)),
            # StaticObstacle((200, 300), shapes.Rectangle, (100, 10)),
            # Vertical segments
            StaticObstacle((200, 0), shapes.Rectangle, (10, 100)),
            StaticObstacle((400, 0), shapes.Rectangle, (10, 200)),
            StaticObstacle((100, 100), shapes.Rectangle, (10, 100)),
            StaticObstacle((300, 200), shapes.Rectangle, (10, 100)),
            StaticObstacle((200, 300), shapes.Rectangle, (10, 100)),
            StaticObstacle((400, 300), shapes.Rectangle, (10, 100)),
            # Horizontal segments
            StaticObstacle((200, 100), shapes.Rectangle, (100, 10)),
            StaticObstacle((100, 200), shapes.Rectangle, (310, 10)),
            StaticObstacle((0, 300), shapes.Rectangle, (200, 10)),
            StaticObstacle((100, 400), shapes.Rectangle, (310, 10)),
        ]
        return


#### Half-converted Layouts
# (layouts that were ported from the old format but never tested)


# Alley
class LayoutAlley(Layout):
    def __init__(self) -> None:
        super().__init__(start=(10, 250), end=(490, 250))
        self.static_obstacles = [
            StaticObstacle((100, 195), shapes.Rectangle, (300, 50)),
            StaticObstacle((100, 250), shapes.Rectangle, (300, 50)),
        ]
        return


# Space
class LayoutSpace(Layout):
    def __init__(self) -> None:
        super().__init__(start=(10, 400), end=(490, 250))
        self.static_obstacles = [
            StaticObstacle((26, 47), shapes.Rectangle, (19, 19)),
            StaticObstacle((362, 50), shapes.Rectangle, (43, 43)),
            StaticObstacle((188, 26), shapes.Rectangle, (50, 50)),
            StaticObstacle((60, 427), shapes.Rectangle, (19, 19)),
            StaticObstacle((261, 327), shapes.Rectangle, (48, 48)),
            StaticObstacle((267, 298), shapes.Rectangle, (10, 10)),
            StaticObstacle((299, 85), shapes.Rectangle, (30, 30)),
            StaticObstacle((353, 368), shapes.Rectangle, (44, 44)),
            StaticObstacle((144, 139), shapes.Rectangle, (11, 11)),
            StaticObstacle((419, 237), shapes.Rectangle, (48, 48)),
            StaticObstacle((349, 460), shapes.Rectangle, (17, 17)),
            StaticObstacle((150, 181), shapes.Rectangle, (32, 32)),
            StaticObstacle((197, 13), shapes.Rectangle, (37, 37)),
            StaticObstacle((143, 72), shapes.Rectangle, (28, 28)),
            StaticObstacle((14, 267), shapes.Rectangle, (33, 33)),
            StaticObstacle((141, 211), shapes.Rectangle, (18, 18)),
            StaticObstacle((469, 88), shapes.Rectangle, (30, 30)),
            StaticObstacle((267, 152), shapes.Rectangle, (14, 14)),
            StaticObstacle((45, 221), shapes.Rectangle, (11, 11)),
            StaticObstacle((201, 110), shapes.Rectangle, (11, 11)),
            StaticObstacle((76, 114), shapes.Rectangle, (21, 21)),
            StaticObstacle((456, 434), shapes.Rectangle, (22, 22)),
            StaticObstacle((239, 177), shapes.Rectangle, (50, 50)),
            StaticObstacle((419, 247), shapes.Rectangle, (10, 10)),
            StaticObstacle((244, 93), shapes.Rectangle, (37, 37)),
            StaticObstacle((286, 291), shapes.Rectangle, (40, 40)),
            StaticObstacle((378, 115), shapes.Rectangle, (50, 50)),
            StaticObstacle((81, 393), shapes.Rectangle, (29, 29)),
            StaticObstacle((379, 121), shapes.Rectangle, (42, 42)),
            StaticObstacle((273, 413), shapes.Rectangle, (33, 33)),
            StaticObstacle((36, 77), shapes.Rectangle, (25, 25)),
            StaticObstacle((429, 236), shapes.Rectangle, (19, 19)),
            StaticObstacle((169, 74), shapes.Rectangle, (43, 43)),
            StaticObstacle((147, 413), shapes.Rectangle, (32, 32)),
            StaticObstacle((467, 432), shapes.Rectangle, (16, 16)),
            StaticObstacle((334, 367), shapes.Rectangle, (21, 21)),
            StaticObstacle((172, 386), shapes.Rectangle, (12, 12)),
            StaticObstacle((131, 413), shapes.Rectangle, (21, 21)),
            StaticObstacle((80, 301), shapes.Rectangle, (40, 40)),
            StaticObstacle((139, 207), shapes.Rectangle, (48, 48)),
            StaticObstacle((112, 228), shapes.Rectangle, (16, 16)),
            StaticObstacle((472, 265), shapes.Rectangle, (24, 24)),
            StaticObstacle((313, 239), shapes.Rectangle, (30, 30)),
            StaticObstacle((376, 353), shapes.Rectangle, (26, 26)),
            StaticObstacle((422, 102), shapes.Rectangle, (26, 26)),
            StaticObstacle((68, 347), shapes.Rectangle, (11, 11)),
            StaticObstacle((62, 371), shapes.Rectangle, (47, 47)),
            StaticObstacle((156, 323), shapes.Rectangle, (32, 32)),
            StaticObstacle((264, 419), shapes.Rectangle, (29, 29)),
            StaticObstacle((19, 337), shapes.Rectangle, (43, 43)),
        ]
        return


## OLD DEFNITIONS


# The Cross - A simple cross-shaped environment
# Testing basic navigation
def layout_simple_cross():
    layout = {
        "size": (500, 500),
        "start": (10, 10),
        "goal": (490, 490),
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


def layout_super_maze():
    layout = {
        "size": (1000, 1000),
        "start": (50, 950),
        "goal": (950, 450),
        "name": "supermaze",
        "obstacles": [
            ((490, 0), (10, 200)),
            ((690, 0), (10, 100)),
            ((790, 0), (10, 300)),
            ((190, 90), (10, 210)),
            ((290, 100), (10, 300)),
            ((390, 100), (10, 200)),
            ((590, 100), (10, 600)),
            ((890, 100), (10, 100)),
            ((90, 190), (10, 110)),
            ((490, 300), (10, 300)),
            ((690, 290), (10, 310)),
            ((390, 400), (10, 100)),
            ((790, 390), (10, 110)),
            ((90, 490), (10, 110)),
            ((890, 500), (10, 300)),
            ((190, 590), (10, 110)),
            ((390, 600), (10, 100)),
            ((490, 700), (10, 100)),
            ((690, 700), (10, 300)),
            ((190, 790), (10, 110)),
            ((390, 800), (10, 100)),
            ((790, 800), (10, 100)),
            ((290, 900), (10, 100)),
            ((490, 890), (10, 110)),
            ((0, 90), (100, 10)),
            ((0, 290), (100, 10)),
            ((0, 690), (200, 10)),
            ((0, 790), (100, 10)),
            ((100, 190), (100, 10)),
            ((100, 390), (300, 10)),
            ((100, 490), (300, 10)),
            ((100, 890), (100, 10)),
            ((200, 90), (100, 10)),
            ((200, 590), (200, 10)),
            ((200, 790), (400, 10)),
            ((300, 690), (200, 10)),
            ((400, 290), (200, 10)),
            ((500, 890), (100, 10)),
            ((600, 190), (100, 10)),
            ((600, 690), (200, 10)),
            ((700, 290), (100, 10)),
            ((700, 590), (200, 10)),
            ((800, 190), (100, 10)),
            ((800, 390), (200, 10)),
            ((800, 890), (200, 10)),
            ((900, 290), (100, 10)),
        ],
    }
    return layout


##### FIX THIS
# The Spiral - Environment with a spiral of obstacles
# Tests ability to navigate through progressively tighter spaces.
def layout_space():
    layout = {
        "size": (500, 500),
        "start": (10, 400),
        "goal": (490, 250),
        "name": "space",
        "obstacles": [
            ((26, 47), (19, 19)),
            ((362, 50), (43, 43)),
            ((188, 26), (50, 50)),
            ((60, 427), (19, 19)),
            ((261, 327), (48, 48)),
            ((267, 298), (10, 10)),
            ((299, 85), (30, 30)),
            ((353, 368), (44, 44)),
            ((144, 139), (11, 11)),
            ((419, 237), (48, 48)),
            ((349, 460), (17, 17)),
            ((150, 181), (32, 32)),
            ((197, 13), (37, 37)),
            ((143, 72), (28, 28)),
            ((14, 267), (33, 33)),
            ((141, 211), (18, 18)),
            ((469, 88), (30, 30)),
            ((267, 152), (14, 14)),
            ((45, 221), (11, 11)),
            ((201, 110), (11, 11)),
            ((76, 114), (21, 21)),
            ((456, 434), (22, 22)),
            ((239, 177), (50, 50)),
            ((419, 247), (10, 10)),
            ((244, 93), (37, 37)),
            ((286, 291), (40, 40)),
            ((378, 115), (50, 50)),
            ((81, 393), (29, 29)),
            ((379, 121), (42, 42)),
            ((273, 413), (33, 33)),
            ((36, 77), (25, 25)),
            ((429, 236), (19, 19)),
            ((169, 74), (43, 43)),
            ((147, 413), (32, 32)),
            ((467, 432), (16, 16)),
            ((334, 367), (21, 21)),
            ((172, 386), (12, 12)),
            ((131, 413), (21, 21)),
            ((80, 301), (40, 40)),
            ((139, 207), (48, 48)),
            ((112, 228), (16, 16)),
            ((472, 265), (24, 24)),
            ((313, 239), (30, 30)),
            ((376, 353), (26, 26)),
            ((422, 102), (26, 26)),
            ((68, 347), (11, 11)),
            ((62, 371), (47, 47)),
            ((156, 323), (32, 32)),
            ((264, 419), (29, 29)),
            ((19, 337), (43, 43)),
        ],
    }
    return layout


def layout_alley():
    layout = {
        "size": (500, 500),
        "start": (10, 250),
        "goal": (490, 250),
        "name": "alley",
        "obstacles": [
            ((100, 195), (300, 50)),
            ((100, 250), (300, 50)),
        ],
    }
    return layout
