"""idiom-test: idiomatic, dependency-free array transformation helpers for Python.

The goal of this library is to make the everyday reshaping of lists and other
iterables read the way you'd describe it out loud -- ``chunk``, ``flatten``,
``group_by``, ``partition`` -- instead of a pile of nested comprehensions.

Every public function is lazy where it can be, works on any iterable, and never
mutates its input.
"""

from .transforms import (
    chunk,
    compact,
    flatten,
    group_by,
    partition,
    pluck,
    unique,
    window,
)

__all__ = [
    "chunk",
    "compact",
    "flatten",
    "group_by",
    "partition",
    "pluck",
    "unique",
    "window",
]

__version__ = "0.1.0"
