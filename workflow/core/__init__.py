import logging

from functools import wraps


def pipeline(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.before_start()
        self.start()
        func(self, *args, **kwargs)
        self.stop()
        self.after_stop()

    return wrapper

def stage(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        __stage = kwargs.get("__stage")
        if not __stage.get("disable", None):
            self.start(*args, **kwargs)
            func(self, *args, **kwargs)
            self.stop()
        else:
            logging.debug(f"Skipping '{self}' -> '{kwargs.get('__stage')['name']}'")

    return wrapper

def job(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        __job = kwargs.get("__job")
        if not __job.get("disable", None):
            self.start(*args, **kwargs)
            func(self, *args, **kwargs)
            self.stop()
        else:
            logging.debug(f"Skipping '{self}' -> '{kwargs.get('__job')['name']}'")

    return wrapper

def step(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        __step = kwargs.get("__step")
        if not __step.get("disable", None):
            self.start(*args, **kwargs)
            func(self, *args, **kwargs)
            self.stop()
        else:
            logging.debug(f"Skipping '{self}' -> '{kwargs.get('__step')['name']}'")

    return wrapper
