# idiom-test

> Idiomatic, dependency-free array transformation helpers for Python.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status: alpha](https://img.shields.io/badge/status-alpha-orange.svg)](#project-status)

`idiom-test` is a small, pure-Python toolkit for the everyday reshaping of
lists and other iterables. It aims to be the best public-facing library for
common array transformation methods — the operations you reach for constantly
(`chunk`, `flatten`, `group_by`, `partition`, …) but that Python makes you
spell out as nested comprehensions or `itertools` incantations every time.

The whole point is readability: code should say what it does.

```python
import idiom_test as it

# Instead of this...
batches = [data[i:i + 100] for i in range(0, len(data), 100)]

# ...write this.
batches = it.chunk(data, 100)
```

## Why idiom-test?

- **Zero dependencies.** Pure standard-library Python. Nothing to audit, nothing to pin.
- **Never mutates its input.** Every function returns a new object.
- **Lazy where it counts.** Streaming transforms return generators, so they compose on large — even infinite — inputs.
- **Works on any iterable.** Lists, tuples, generators, ranges, files — if you can iterate it, you can transform it.
- **Fully type-hinted.** Ships with inline types for editor autocomplete and `mypy`.

## Installation

```bash
pip install idiom-test
```

Requires Python 3.9 or newer.

> <a name="project-status"></a>**Project status:** `idiom-test` is in early
> (alpha) development. The functions documented below are implemented and
> tested; the API may still change before 1.0. See [Roadmap](#roadmap).

## Quick start

```python
import idiom_test as it

# Split an iterable into fixed-size batches
list(it.chunk([1, 2, 3, 4, 5], 2))
# -> [[1, 2], [3, 4], [5]]

# Flatten nested structures (one level by default, fully with depth=-1)
list(it.flatten([1, [2, [3, [4]]]], depth=-1))
# -> [1, 2, 3, 4]

# De-duplicate while preserving order, optionally by a key
list(it.unique(["Apple", "apple", "Banana"], key=str.lower))
# -> ['Apple', 'Banana']

# Group items by a computed key
it.group_by(range(6), key=lambda n: n % 2)
# -> {0: [0, 2, 4], 1: [1, 3, 5]}

# Split into (matching, non-matching) in a single pass
evens, odds = it.partition(range(6), lambda n: n % 2 == 0)
# -> ([0, 2, 4], [1, 3, 5])

# Pull a field out of every item (dicts or objects)
list(it.pluck([{"id": 1}, {"id": 2}], "id"))
# -> [1, 2]
```

## API reference

All functions live at the top level of the `idiom_test` package. Those that can
stream return an iterator (wrap in `list(...)` to materialise); the rest return
a concrete container.

| Function | Signature | Description |
| --- | --- | --- |
| `chunk` | `chunk(iterable, size) -> Iterator[list]` | Split into consecutive lists of at most `size` items. |
| `flatten` | `flatten(iterable, depth=1) -> Iterator` | Flatten nesting up to `depth` levels (`-1` = fully). Strings/bytes stay atomic. |
| `compact` | `compact(iterable) -> Iterator` | Drop falsy values (`None`, `0`, `""`, `False`, …). |
| `unique` | `unique(iterable, key=None) -> Iterator` | Yield first occurrences in order, optionally keyed. |
| `group_by` | `group_by(iterable, key) -> dict[K, list]` | Group items into a dict by `key(item)`, preserving order. |
| `partition` | `partition(iterable, predicate) -> tuple[list, list]` | Split into `(matching, non_matching)` in one pass. |
| `pluck` | `pluck(iterable, key) -> Iterator` | Extract `item[key]`, falling back to `getattr(item, key)`. |
| `window` | `window(iterable, size) -> Iterator[tuple]` | Yield overlapping sliding windows of length `size`. |

## Roadmap

`idiom-test` is just getting started. Planned additions include:

- More reshaping helpers: `flatten_dict`, `interleave`, `zip_with`, `scan`.
- Set-style combinators: `intersection`, `difference`, `symmetric_difference` with `key=` support.
- A fluent, chainable pipeline API (`it.pipe(data).chunk(2).flatten()`).
- Optional acceleration paths for very large inputs.

Have a transformation you use all the time? [Open an issue](https://github.com/wholelottatesting/idiom-test/issues) and let's add it.

## Development

```bash
git clone https://github.com/wholelottatesting/idiom-test.git
cd idiom-test
python -m pip install -e ".[dev]"
pytest
```

The test suite runs the unit tests in `tests/` together with the docstring
examples in the source (`--doctest-modules`), so the examples above are
guaranteed to stay correct.

## Contributing

Contributions are welcome! Please:

1. Open an issue to discuss non-trivial changes first.
2. Keep the library dependency-free and fully type-hinted.
3. Add tests (and doctests for user-facing examples) for anything you add.
4. Run `pytest` before submitting a pull request.

## License

Released under the [MIT License](LICENSE).
