"""module contains datastructures needed to create the @debounce decorator."""
import time
from functools import wraps, partial
from pythonicqt.Qt import QtCore

class DebounceTimer(QtCore.QTimer):
    """Used with the debounce decorator, used for delaying/throttling calls."""
    def __init__(self, msecs, fire_on_first=False, ignore_delayed=False):
        self.is_setup = False
        self.msecs_interval = msecs
        self.seconds_interval = msecs / 1000.0
        self.last_update = time.time() - self.seconds_interval - 1
        self.delayed_call = False
        self.fire_on_first = fire_on_first
        self.ignore_delayed = ignore_delayed

    def setup_parent(self, parent):
        """Needs the parent before this object can be setup."""
        self.is_setup = True
        QtCore.QTimer.__init__(self, parent)
        self.timeout.connect(self.call_function)
        self.setInterval(self.msecs_interval)
        self.start()
        
    def call_function(self, *args):
        """On timeout calls the delayed function if neccessary."""
        self.stop()
        if self.delayed_call:
            self.delayed_call()
            self.delayed_call = False
            self.last_update = time.time()
        self.start(self.msecs_interval)

def debounce(msecs, fire_on_first=False, ignore_delayed=False):
    """Decorator that prevents a function from being called more than once every
    time period between calls. Postpones execution when threshold is breached.
    If fire_on_first is True, calls are immediately propagated after the time threshold 
    passes, else the first calls are allows made after an entire msecs period after the
    most recent call. 
        @debounce(msecs=1)
        def my_fun(self):
            pass
    """
    def wrap_wrapper(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            if not hasattr(instance, "__debounce_dict"):
                instance.__debounce_dict = {}
            if func not in instance.__debounce_dict:
                new_timer = DebounceTimer(msecs, fire_on_first=fire_on_first, ignore_delayed=ignore_delayed)
                instance.__debounce_dict[func] = new_timer
                new_timer.setup_parent(instance)
            debounce_timer = instance.__debounce_dict[func]
            debounce_timer.stop()
            difference = time.time() - debounce_timer.last_update 
            if difference > debounce_timer.seconds_interval and debounce_timer.fire_on_first:
                debounce_timer.delayed_call = False
                func(instance, *args, **kwargs)
                debounce_timer.last_update = time.time()
            else:
                if not debounce_timer.ignore_delayed:
                    debounce_timer.delayed_call = partial(func, instance, *args, **kwargs)
            debounce_timer.start(debounce_timer.msecs_interval)
        return wrapper
    return wrap_wrapper