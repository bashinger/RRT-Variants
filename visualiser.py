import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from Layout import Layout
from Shapes import Circle
from Obstacle import Obstacle


class Visualiser:
    def __init__(
        self,
        layout=None,
    ):
        if layout is not None:
            self.size = layout.get("size", (500, 500))
            self.start = layout.get("start", (10, 10))
            self.goal = layout.get("goal", (480, 480))
            self.obstacles = layout.get("obstacles", [])
        else:
            # Set defaults if no layout is provided
            self.size = (500, 500)
            self.start = (10, 10)
            self.goal = (480, 480)
            self.obstacles = []

    def preview_layout(self):
        fig, ax = self._setup_plot()
        self._draw_obstacles(ax)
        self._draw_points(ax, [self.start], "go", "Start")  # Start in green
        self._draw_points(ax, [self.goal], "bo", "Goal")  # Goal in blue
        plt.show()

    def visualize_gaussian_cloud(self, path, ref, nodes):
        fig, ax = self._setup_plot()
        self._draw_obstacles(ax)
        self._draw_path(ax, path)
        self._draw_points(ax, [n for n in nodes], "c.", "Gaussian Nodes")
        self._draw_points(ax, [ref], "mo", "Reference Node")
        self._draw_points(ax, [self.start], "go", "Start")
        self._draw_points(ax, [self.goal], "bo", "Goal")
        plt.show()

    def visualize_path(self, nodes, path):
        fig, ax = self._setup_plot()
        self._draw_obstacles(ax)
        self._draw_tree(ax, nodes)
        self._draw_path(ax, path)
        self._draw_points(ax, [self.start], "g.", "Start")
        self._draw_points(ax, [self.goal], "b.", "Goal")
        plt.show()

    def _setup_plot(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.size[0])
        ax.set_ylim(0, self.size[1])
        ax.set_aspect("equal")
        ax.set_title("Map Environment")
        return fig, ax

    def _draw_obstacles(self, ax):
        for obstacle in self.obstacles:
            ox, oy = obstacle[0]
            width, height = obstacle[1]
            rect = patches.Rectangle((ox, oy), width, height, linewidth=1, facecolor="black")
            ax.add_patch(rect)

    def _draw_tree(self, ax, nodes):
        for node in nodes:
            if node.parent is not None:
                ax.plot(
                    [node.position[0], node.parent.position[0]],
                    [node.position[1], node.parent.position[1]],
                    "r-",
                    linewidth=0.4,
                )

    def _draw_path(self, ax, path):
        if path:
            ax.plot([p[0] for p in path], [p[1] for p in path], "-b.", linewidth=0.8, label="Path", markersize=2.5)

    def _draw_points(self, ax, points, style, label=None):
        for point in points:
            ax.plot(point[0], point[1], style, markersize=5, label=label)
        if label:
            ax.legend(loc="upper left", bbox_to_anchor=(1, 1))


class DynamicVisualiser:
    """
    Self-updating visualiser that continuously shows a map env.
    """

    render_freq: int
    """
    The frequency (in ms) at which the visualiser updates.
    """
    update_interval: float
    """
    The interval (in seconds) at which the objects move.
    """

    fig: Figure
    ax: Axes
    layout: Layout
    anim: FuncAnimation
    actors: list[patches.Patch]

    def __init__(self, render_freq: int, layout: Layout) -> None:
        """
        Parameters:
        ----------
        - `render_freq`: float
            The frequency (in ms) at which the obstacles move.
        - `layout`: Type[DynamicLayout]
            The layout of the map.
        """
        self.layout = layout
        self.render_freq = render_freq
        self.update_interval = render_freq / 10e3
        self.fig, self.ax = plt.subplots()
        self.actors = []

        # set up plot
        self.ax.set_xlim(0, self.layout.size[0])
        self.ax.set_ylim(0, self.layout.size[1])
        self.ax.set_aspect("equal")
        self.ax.set_title("Map Environment")
        self.ax.plot(*self.layout.start, "go", markersize=5, label="Start")
        self.ax.plot(*self.layout.end, "bo", markersize=5, label="Goal")
        self.ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

        # initialise static obstacles
        for obstacle in self.layout.static_obstacles:
            self.ax.add_patch(
                patches.Rectangle(
                    tuple(obstacle.anchor_point.components[:2]),
                    obstacle.shape.width,
                    obstacle.shape.height,
                    linewidth=5,
                    facecolor="black",
                )
            )

        # initialise dynamic obstacles
        for obstacle in self.layout.dynamic_obstacles:
            if type(obstacle.shape) is Circle:
                actor = patches.Circle(
                    tuple(obstacle.anchor_point.components[:2]), obstacle.shape.radius, linewidth=1, facecolor="red"
                )
                print(f"adding obstacle: {tuple(obstacle.anchor_point.components[:2])}")
                actor.set_animated(True)
                self.ax.add_patch(actor)
                self.actors.append(actor)

        # blit is an optimistic graphics optimisation (not available on all platforms)
        # no harm if unavailable
        self.anim = FuncAnimation(
            self.fig, func=self.update, interval=self.render_freq, blit=True, cache_frame_data=True, save_count=50
        )
        plt.show()
        return

    def update(self, frame) -> list[patches.Patch]:
        """
        Update the positions of the obstacles.
        """

        obstacles: list[Obstacle] = self.layout.dynamic_obstacles + self.layout.static_obstacles
        if len(self.layout.dynamic_obstacles) != len(self.actors):
            raise IndexError("Number of obstacles seems to have changed during simulation")
        for obstacle, actor in zip(self.layout.dynamic_obstacles, self.actors):
            obstacle.move(self.update_interval)
            for other_obstacle in obstacles:
                if obstacle != other_obstacle and obstacle.is_new_collision(other_obstacle):
                    obstacle.ricochet(other_obstacle)
            actor.set(center=tuple(obstacle.anchor_point.components[:2]))
        return self.actors
