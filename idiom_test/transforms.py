"""Core array transformation functions.

All functions accept any iterable and return a new object; inputs are never
mutated. Functions that can stream their results return a generator so they
compose cleanly on large or infinite inputs.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable, Iterator
from itertools import islice
from typing import Any, TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)

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


def chunk(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield successive lists of at most ``size`` items.

    >>> list(chunk([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    """
    if size < 1:
        raise ValueError("size must be a positive integer")
    iterator = iter(iterable)
    while batch := list(islice(iterator, size)):
        yield batch


def flatten(iterable: Iterable[Any], depth: int = 1) -> Iterator[Any]:
    """Flatten a nested iterable up to ``depth`` levels.

    Strings and bytes are treated as atomic values, not iterables.

    >>> list(flatten([1, [2, [3, [4]]]]))
    [1, 2, [3, [4]]]
    >>> list(flatten([1, [2, [3, [4]]]], depth=-1))
    [1, 2, 3, 4]
    """
    for item in iterable:
        if depth != 0 and isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item, depth - 1)
        else:
            yield item


def compact(iterable: Iterable[T]) -> Iterator[T]:
    """Yield only the truthy items, dropping ``None``, ``0``, ``""`` and friends.

    >>> list(compact([0, 1, False, 2, "", 3, None]))
    [1, 2, 3]
    """
    return (item for item in iterable if item)


def unique(iterable: Iterable[T], key: Callable[[T], Hashable] | None = None) -> Iterator[T]:
    """Yield items in order, skipping ones already seen.

    An optional ``key`` selects the value used for the uniqueness check.

    >>> list(unique([1, 1, 2, 3, 3, 3, 1]))
    [1, 2, 3]
    >>> list(unique(["Apple", "apple", "Banana"], key=str.lower))
    ['Apple', 'Banana']
    """
    seen: set[Hashable] = set()
    for item in iterable:
        marker = key(item) if key is not None else item
        if marker not in seen:
            seen.add(marker)
            yield item


def group_by(iterable: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group items into a dict keyed by ``key(item)``, preserving order.

    >>> group_by(range(6), key=lambda n: n % 2)
    {0: [0, 2, 4], 1: [1, 3, 5]}
    """
    groups: dict[K, list[T]] = defaultdict(list)
    for item in iterable:
        groups[key(item)].append(item)
    return dict(groups)


def partition(
    iterable: Iterable[T], predicate: Callable[[T], bool]
) -> tuple[list[T], list[T]]:
    """Split into ``(matching, non_matching)`` lists based on ``predicate``.

    >>> partition(range(6), lambda n: n % 2 == 0)
    ([0, 2, 4], [1, 3, 5])
    """
    matching: list[T] = []
    non_matching: list[T] = []
    for item in iterable:
        (matching if predicate(item) else non_matching).append(item)
    return matching, non_matching


def pluck(iterable: Iterable[Any], key: Hashable) -> Iterator[Any]:
    """Extract ``item[key]`` (or ``getattr(item, key)``) from each item.

    Mapping lookups are tried first, then attribute access, so it works on both
    dicts and objects.

    >>> list(pluck([{"id": 1}, {"id": 2}], "id"))
    [1, 2]
    """
    for item in iterable:
        try:
            yield item[key]
        except (TypeError, KeyError, IndexError):
            yield getattr(item, key)  # type: ignore[arg-type]


def window(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """Yield overlapping tuples of length ``size`` (a sliding window).

    >>> list(window([1, 2, 3, 4], 2))
    [(1, 2), (2, 3), (3, 4)]
    """
    if size < 1:
        raise ValueError("size must be a positive integer")
    iterator = iter(iterable)
    current = tuple(islice(iterator, size))
    if len(current) == size:
        yield current
    for item in iterator:
        current = current[1:] + (item,)
        yield current
