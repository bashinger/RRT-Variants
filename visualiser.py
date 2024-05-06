from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.patches as patches
from matplotlib.artist import Artist
from matplotlib.animation import FuncAnimation
from map import Map
from shapes import Circle
from obstacle import Obstacle


class Visualiser:
    """
    Visualiser that shows a map
    """

    map: Map
    fig: Figure
    ax: Axes

    def __init__(self, map: Map) -> None:
        self.map = map
        self.fig, self.ax = plt.subplots()
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
                self.ax.add_patch(
                    patch_type(
                        tuple(obstacle.anchor_point.components[:2]),
                        *shape_args,
                        linewidth=1,
                        facecolor="red",
                    )
                )
            except AttributeError:
                raise ValueError(f"Shape unsupported by `matplotlib`: {obstacle.shape.__class__.__name__}")

        # draw the tree
        for node in self.map.nodes:
            if node.parent is not None:
                self.ax.plot(
                    [node.position.components[0], node.parent.position.components[0]],
                    [node.position.components[1], node.parent.position.components[1]],
                    "-r.",
                    linewidth=0.4,
                )

        # draw the path
        if self.map.path is not None:
            self.ax.plot(
                [node.position.components[0] for node in self.map.path],
                [node.position.components[1] for node in self.map.path],
                "-b.",
                linewidth=0.8,
            )

        plt.show(block=True)
        return

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
    actors: list[Artist]
    last_plotted_index: int

    def __init__(self, render_freq: int, map: Map, rrt) -> None:
        """
        Parameters:
        ----------
        - `render_freq`: float
            The frequency (in ms) at which the obstacles move.
        - `layout`: Type[DynamicLayout]
            The layout of the map.
        """
        self.map = map
        self.rrt = rrt
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

        # update last_plotted_index to reflect start node having been plotted
        self.last_plotted_index = len(self.map.nodes) - 1

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
        plt.show(block=True)
        return

    def update(self, frame) -> list[Line2D]:
        """
        Update the positions of the obstacles.
        """

        # # lock the map in its current state to maintain consistency
        # self.map.lock.acquire(blocking=True)
        # self.map.lock.wait_for(lambda: self.map.locked)

        lines: list[Line2D] = []

        # update the last plotted index
        last_plotted_index = len(self.map.nodes) - 1
        self.rrt.seek_new_candidate()
        # print(f"Last plotted index: {last_plotted_index}")

        # plot the newly added nodes that haven't yet been plotted
        for node in self.map.nodes[self.last_plotted_index + 1:last_plotted_index + 1]:
            if node.parent is None:
                raise ValueError("The planner algorithm seems to have appended a floating node")
            lines += self.ax.plot(
                [node.position.components[0], node.parent.position.components[0]],
                [node.position.components[1], node.parent.position.components[1]],
                "-r.",
                linewidth=0.4,
                markersize=2,
            )
                # [self.ax.add_line(line) for line in lines]
                # self.actors.append(lines)

        # # update the dynamic obstacles
        # if len(self.map.dynamic_obstacles) != len(self.actors):
        #     raise IndexError("Number of dynamic obstacles seems to have changed during simulation")
        # for obstacle, actor in zip(self.map.dynamic_obstacles, self.actors):
        #     actor.set(center=tuple(obstacle.anchor_point.components[:2]))

        # if the path has been found, draw the optimal path and pause the animation
        if self.map.path is not None:
            lines += self.ax.plot(
                [node.position.components[0] for node in self.map.path],
                [node.position.components[1] for node in self.map.path],
                "-b.",
                linewidth=0.8,
                markersize=2,
            )
            # self.actors.append(lines)
            # [self.ax.add_line(line) for line in lines]
            self.anim.pause()

        # # release the lock
        # self.map.lock.notify()
        # self.map.lock.release()

        return lines
