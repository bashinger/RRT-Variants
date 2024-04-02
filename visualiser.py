import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from map import Map
from shapes import Circle
from obstacle import Obstacle


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
    map: Map
    anim: FuncAnimation
    actors: list[patches.Patch]

    def __init__(self, render_freq: int, map: Map) -> None:
        """
        Parameters:
        ----------
        - `render_freq`: float
            The frequency (in ms) at which the obstacles move.
        - `layout`: Type[DynamicLayout]
            The layout of the map.
        """
        self.map = map
        self.render_freq = render_freq
        self.update_interval = render_freq / 10e3
        self.fig, self.ax = plt.subplots()
        self.actors = []

        # set up plot
        self.ax.set_xlim(0, self.map.size[0])
        self.ax.set_ylim(0, self.map.size[1])
        self.ax.set_aspect("equal")
        self.ax.set_title("Map Environment")
        self.ax.plot(*self.map.start.position.components[:2], "go", markersize=5, label="Start")
        self.ax.plot(*self.map.end.position.components[:2], "bo", markersize=5, label="Goal")
        self.ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

        # initialise static obstacles
        for obstacle in self.map.static_obstacles:
            try:
                patch_type = getattr(patches, obstacle.shape.__class__.__name__)
                shape_args = obstacle.shape.get_attrs()
                self.ax.add_patch(
                    patch_type(
                        tuple(obstacle.anchor_point.components[:2]),
                        *shape_args,
                        linewidth=5,
                        facecolor="black",
                    )
                )
            except AttributeError:
                raise ValueError(f"Shape unsupported by `matplotlib`: {obstacle.shape.__class__.__name__}")

        # initialise dynamic obstacles
        for obstacle in self.map.dynamic_obstacles:
            try:
                patch_type = getattr(patches, obstacle.shape.__class__.__name__)
                shape_args = obstacle.shape.get_attrs()
                actor = patch_type(
                    tuple(obstacle.anchor_point.components[:2]), *shape_args, linewidth=1, facecolor="red"
                )
                actor.set_animated(True)
                self.ax.add_patch(actor)
                self.actors.append(actor)
            except AttributeError:
                raise ValueError(f"Shape unsupported by `matplotlib`: {obstacle.shape.__class__.__name__}")

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

        self.map.update(self.update_interval)
        if len(self.map.dynamic_obstacles) != len(self.actors):
            raise IndexError("Number of dynamic obstacles seems to have changed during simulation")
        for obstacle, actor in zip(self.map.dynamic_obstacles, self.actors):
            actor.set(center=tuple(obstacle.anchor_point.components[:2]))
        return self.actors
