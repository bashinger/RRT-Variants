'''
A debug kit for path planners in this project
Lets you 'pause' the planner at any point in time and inspect its state
'''

# TODO: we need an abstract planner (implementing a `find_path` method)
# this assumes it's called `RRT`
#from rrt import RRT

# Summary
# ---===---

# class Interjektor(Thread)
# A generic daemon thread that pauses another thread on keypress

# @debug_planner
# A decorator that pauses a planner on keypress, letting one inspect its state
# TODO:
#   - fix `matplotlib` visualiser to inspect state when paused
#   - kill the planner on special sequences (^C, ^D)
# USAGE:
# N.B.: if <func> to be paused is a class's method, use `self.<func>` below
#   - at the beginning of the function, include:
#     `[self.]<func>.pause_condition.acquire()`
#   - *immediately prior* to the loop that is to be pausable,
#     signal the pauser that the loop is about to begin with:
#     `[self.]<func>.pause_condition.notify()`
#     `[self.]<func>.pause_condition.release()`
#   - at the beginning of the looping code, include:
#     `self.find_path.pause_condition.acquire(blocking=True)`
#     `self.find_path.pause_condition.wait_for(lambda: not self.find_path.paused)`
#   - at the end of the looping code, include:
#     `self.find_path.pause_condition.release()`

# @proc_time
# A simple decorator that times a function in terms of CPU time consumed
# and prints the result to `stderr`

wait_for_keypress_cmd: list[str]
'''
An OS-specific command that waits for a keypress (Windows/POSIX dependant)
'''

# Imports
# ---===---
from os import system as run_cmd
from sys import stdin, stderr
from time import process_time_ns
from platform import system
from threading import Thread, Condition, Event
from subprocess import Popen, DEVNULL
from multiprocessing import Process # matplotlib doesn't like being in a subthread

# Definitions
# ---===---
class Interjektor(Thread):
    '''
    A generic daemon thread that pauses another thread on keypress
    '''

    __blocker: Popen | None
    '''
    An OS-dependent subprocess that blocks until keypress
    '''

    __must_exit: Event
    '''
    An `Event` primitive that serves as a sign to terminate the thread,
    and is checked by the thread.
    '''

    class _Harakiri(Exception):
        '''
        An exception that is raised when the thread must terminate
        '''
        pass

    def __init__(self, pause_condition: Condition, is_paused: bool, **kwargs): # planner: the RRT object
        super().__init__(daemon=True, **kwargs)
        self.__blocker = None
        self.__must_exit = Event()
        self.pause_condition = pause_condition
        self.is_paused = is_paused
        return

    def run(self):
        # wait for the planner to start running
        self.pause_condition.acquire(blocking=True)
        print("DEBUG: Waiting for the planner loop to start running...", file=stderr)
        self.pause_condition.wait()
        self.pause_condition.release()

        while not self.is_paused:
            try:
                self._pause_on_keypress()
            except self._Harakiri:
                # we were meant to die
                return

            self._resume_on_keypress()
        return

    def stop(self):
        self.__must_exit.set()
        self.__blocker.terminate() if self.__blocker is not None else None
        return

    # helpers:
    # --------
    def _pause_on_keypress(self):
        # block until user hits a key
        print("Press any key to pause...", end="", flush=True, file=stderr)
        self.__blocker = Popen(wait_for_keypress_cmd, stdin=stdin, stdout=DEVNULL, stderr=DEVNULL)
        self.__blocker.wait()
        print(flush=True)
        if self.__must_exit.is_set():
            raise self._Harakiri()
            return

        # if we reach here, the keypress detector was either activated,
        # or killed somehow (e.g. through ^C, or externally)
        # former means the planner must be paused
        # TODO: handle the latter specially (e.g. terminate)
        print("Pausing...", file=stderr)
        self.is_paused = True
        self.pause_condition.acquire(blocking=True) # wait for consistent state
        return

    def _resume_on_keypress(self):
        print("Press any key to resume...", end="", flush=True)
        self.__blocker = Popen(wait_for_keypress_cmd, stdin=stdin, stdout=DEVNULL, stderr=DEVNULL)
        self.__blocker.wait()
        print(flush=True)
        self.is_paused = False
        self.pause_condition.notify()
        self.pause_condition.release()
        return

class Sauron(Interjektor):
    '''
    A daemon thread that pauses a running planner on keypress,
    and lets one inspect its state.
    For internal use by `debug_planner` only
    '''

    def __init__(self, planner, *args, **kwargs): # planner: the RRT object
        super().__init__(*args, **kwargs)
        self.planner = planner
        return

    def run(self):
        # wait for the planner to start running
        self.pause_condition.acquire(blocking=True)
        print("DEBUG: Waiting for the planner loop to start running...", file=stderr)
        self.pause_condition.wait()
        self.pause_condition.release()

        while not self.is_paused:
            try:
                self._pause_on_keypress()
            except self._Harakiri:
                # we were meant to die
                return

            # print the current state
            goal = self.planner.map_env.goal
            print(
                "Current minimum distance to node: ",
                self.planner.distance(
                    self.planner.nearest_node(goal).position, goal
                ),
                file=stderr
            )

            # draw the current state
            sauron = Process(
                target=self.planner.map_env.visualize_path,
                args=(
                    self.planner.nodes, self.planner._trace_path(self.planner.nodes[-1])
                )
            )
            sauron.start()
            sauron.join()

            # when called from a script, matplotlib will not block
            # workaround: use a keypress detector again
            # ! this doesn't seem to be true, but resume on keypress is nice?
            self._resume_on_keypress()
        return

def pauseable(func): # planner: RRT.find_path()
    '''
    A decorator that pauses a (properly set up) function on keypress
    '''
    is_paused: bool = False
    pause_condition = Condition()
    # blocker: Popen | None = None

    def wrapper(*args, **kwargs):     # planner_self_obj: an RRT (abstract)
        pauser_daemon = Interjektor(pause_condition, is_paused)
        pauser_daemon.start()
        result = func(*args, **kwargs)
        print(f"DEBUG: The function '{func.__name__}' has finished running.", file=stderr)
        pauser_daemon.stop()
        return result

    wrapper.paused = is_paused
    wrapper.pause_condition = pause_condition
    return wrapper


def debug_planner(planner_func): # planner: RRT.find_path()
    '''
    A decorator that pauses a planner on keypress, letting one inspect its state
    '''
    is_paused: bool = False
    pause_condition = Condition()
    # blocker: Popen | None = None

    def wrapper(planner_self_obj, *args, **kwargs):     # planner_self_obj: an RRT (abstract)
        pauser_daemon = Sauron(planner_self_obj, pause_condition, is_paused)
        pauser_daemon.start()
        result = planner_func(planner_self_obj, *args, **kwargs)
        print("DEBUG: The planner has finished running.", file=stderr)
        pauser_daemon.stop()
        return result

    wrapper.paused = is_paused
    wrapper.pause_condition = pause_condition
    return wrapper

def proc_time(func):
    def wrapper(*args, **kwargs):
        start_time = process_time_ns()
        result = func(*args, **kwargs)
        end_time = process_time_ns()
        args_str = [str(a.__class__) for a in args]
        kwargs_str = [f"{k}={str(v.__class__)}" for k, v in kwargs.items()]
        signature = ", ".join(args_str + kwargs_str)
        print(f"DEBUG: {func.__name__}({signature}) took {float(end_time - start_time)/10e3:,.3g} µs", file=stderr)
        return result
    return wrapper

# Other Definitions
# ---===---
# OS-specific shenanigans
if system() == "Windows":
    wait_for_keypress_cmd = ['@pause']
else:
    wait_for_keypress_cmd = ['/bin/bash', '-c', 'read -s -n 1']
