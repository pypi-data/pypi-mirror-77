"""
Wrapper module for sequential task (continuation) handling.
Use as fallback for _tasks_async when async/await is not available.
"""
from types import GeneratorType


class UpdateTask:
    "Wrap a generator in a task-like interface"

    def __init__(self, gen, desc):
        """
        Arguments:
            - gen: generator object
            - desc<tuple>: (Resource, key)
        """
        assert isinstance(gen, GeneratorType)
        self._gen = gen
        self._desc = desc

    def __repr__(self):
        res, pk = self._desc
        return "<UpdateTask: ({}, {})>".format(res.tag, pk)

    def cancel(self):
        pass

    def __iter__(self):
        return self._gen

    def send(self, x):
        return self._gen.send(x)


def gather(jobs):
    "Aggregate and collect jobs"
    for job in jobs:
        yield from job


def wrap_generator(func):
    "Identity decorator (only needed for async compatibility)"
    return func


def _consume_task_or_generator(item):
    if isinstance(item, (GeneratorType, UpdateTask)):
        return _consume_task(item)
    else:
        return item


def _consume_task(gen):
    r, ret = None, []
    while True:
        try:
            item = gen.send(r)
        except StopIteration:
            break
        r = _consume_task_or_generator(item)
        ret.append(r)

    if len(ret) == 1:
        return ret.pop()
    return ret


def run_task(func):
    """
    Decorator to collect and return generator results, returning a list
    if there are multiple results
    """

    def _wrapped(*a, **k):
        gen = func(*a, **k)
        return _consume_task(gen)

    return _wrapped
