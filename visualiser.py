import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
        self._draw_points(ax, [self.start], "go", "Start")
        self._draw_points(ax, [self.goal], "bo", "Goal")
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
                )

    def _draw_path(self, ax, path):
        if path:
            ax.plot(
                [p[0] for p in path],
                [p[1] for p in path],
                "b-",
                linewidth=2,
                label="Path",
            )

    def _draw_points(self, ax, points, style, label=None):
        for point in points:
            ax.plot(point[0], point[1], style, markersize=10, label=label)
        if label:
            # ax.legend(loc="upper left")
            ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

class DynamicVisualiser:
    '''
    Self-updating visualiser that continuously shows a map env.
    '''

    update_freq_time: float
    update_res: int

    def __init__(self, freq: float, ) -> None:
        raise NotImplementedError
