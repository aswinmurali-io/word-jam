import time
import functools

from colorama import init, Fore, Style
from kivy.logger import Logger

init(autoreset=True)


# This function is used to measure the time take by different functions
# both timing and timeit do the same thing but different ways.
# timing -> does not work with kivy
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        Logger.debug(
            Style.DIM
            + "Speed: function "
            + Fore.CYAN
            + Style.NORMAL
            + f.__name__
            + "() "
            + Style.DIM
            + " -> "
            + Fore.RED
            + str((time2 - time1) * 1000.0)
            + "ms"
            + Fore.RESET
        )
        return ret

    return wrap


# kivy_timing -> works with kivy
def kivy_timing(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        Logger.debug(
            Style.DIM
            + "Speed: function "
            + Fore.CYAN
            + Style.NORMAL
            + func.__name__
            + "() "
            + Style.DIM
            + " -> "
            + Fore.RED
            + str(round(elapsedTime * 1000))
            + "ms"
            + Fore.RESET
        )

    return newfunc
