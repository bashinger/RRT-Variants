'''
A debug kit for path planners in this project
Lets you 'pause' the planner at any point in time and inspect its state
'''

# TODO: we need an abstract planner (implementing a `find_path` method)
# this assumes it's called `RRT`
#from rrt import RRT

# Summary
# ---===---

# @debug_planner
# A decorator that pauses a planner on keypress, letting one inspect its state
# TODO:
#   - fix `matplotlib` visualiser to inspect state when paused
#   - kill the planner on special sequences (^C, ^D)

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

def debug_planner(planner_func): # planner: RRT.find_path()
    '''
    A decorator that pauses a planner on keypress, letting one inspect its state
    '''
    is_paused: bool = False
    pause_condition = Condition()
    # blocker: Popen | None = None

    class Interjektor(Thread):
        '''
        A daemon thread that pauses another thread on keypress
        For internal use by `debug_planner` only
        '''
        __blocker: Popen | None
        __must_exit: Event

        def __init__(self, planner): # planner: the RRT object
            super().__init__(daemon=True)
            self.planner = planner
            self.__blocker = None
            self.__must_exit = Event()
            return

        def run(self):
            nonlocal pause_condition, is_paused
            # wait for the planner to start running
            pause_condition.acquire(blocking=True)
            print("DEBUG: Waiting for the planner loop to start running...", file=stderr)
            pause_condition.wait()
            pause_condition.release()

            while not is_paused:
                # block until user hits a key
                print("Press any key to pause...", end="", flush=True, file=stderr)
                self.__blocker = Popen(wait_for_keypress_cmd, stdin=stdin, stdout=DEVNULL, stderr=DEVNULL)
                self.__blocker.wait()
                if self.__must_exit.is_set():
                    return

                # if we reach here, the keypress detector was either activated,
                # or killed somehow (e.g. through ^C, or externally)
                # former means the planner must be paused
                # TODO: handle the latter specially (e.g. terminate)
                print("Pausing...", file=stderr)
                is_paused = True
                pause_condition.acquire(blocking=True) # wait for consistent state

                # draw the current state
                sauron = Process(
                    target=self.planner.map_env.visualize_path,
                    args=(
                        self.planner.nodes, self.planner._trace_path(self.planner.nodes[-1])
                    )
                )
                sauron.start()
                sauron.join()
                # print("Current node list:\n", planner.nodes)
                goal = self.planner.map_env.goal
                print(
                    "Current minimum distance to node: ",
                    self.planner.distance(
                        self.planner.nearest_node(goal).position, goal
                    ),
                    file=stderr
                )

                # when called from a script, matplotlib will not block
                # workaround: use a keypress detector again
                print("Press any key to resume...", end="", flush=True)
                self.__blocker = Popen(wait_for_keypress_cmd, stdin=stdin, stdout=DEVNULL, stderr=DEVNULL)
                self.__blocker.wait()
                is_paused = False
                pause_condition.notify()
                pause_condition.release()
            return

        def stop(self):
            self.__must_exit.set()
            self.__blocker.terminate() if self.__blocker is not None else None


    def wrapper(planner_self_obj, *args, **kwargs):                  # self: an RRT (abstract)
        #nonlocal is_paused, pause_condition
        pauser_daemon = Interjektor(planner_self_obj)
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
