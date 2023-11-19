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
        self.start(*args, **kwargs)
        func(self, *args, **kwargs)
        self.stop()

    return wrapper

def job(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.start(*args, **kwargs)
        func(self, *args, **kwargs)
        self.stop()

    return wrapper

def step(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.start(*args, **kwargs)
        func(self, *args, **kwargs)
        self.stop()

    return wrapper
