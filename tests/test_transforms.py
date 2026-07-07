import pytest

import idiom_test as it


def test_chunk_splits_into_sized_batches():
    assert list(it.chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_chunk_rejects_non_positive_size():
    with pytest.raises(ValueError):
        list(it.chunk([1, 2, 3], 0))


def test_flatten_one_level_by_default():
    assert list(it.flatten([1, [2, [3]]])) == [1, 2, [3]]


def test_flatten_fully_with_negative_depth():
    assert list(it.flatten([1, [2, [3, [4]]]], depth=-1)) == [1, 2, 3, 4]


def test_flatten_treats_strings_as_atoms():
    assert list(it.flatten(["ab", ["cd"]])) == ["ab", "cd"]


def test_compact_drops_falsy_values():
    assert list(it.compact([0, 1, False, 2, "", 3, None])) == [1, 2, 3]


def test_unique_preserves_first_seen_order():
    assert list(it.unique([1, 1, 2, 3, 3, 1])) == [1, 2, 3]


def test_unique_with_key():
    assert list(it.unique(["Apple", "apple", "Banana"], key=str.lower)) == ["Apple", "Banana"]


def test_group_by_preserves_insertion_order():
    assert it.group_by(range(6), key=lambda n: n % 2) == {0: [0, 2, 4], 1: [1, 3, 5]}


def test_partition_returns_matching_then_rest():
    assert it.partition(range(6), lambda n: n % 2 == 0) == ([0, 2, 4], [1, 3, 5])


def test_pluck_from_mappings_and_objects():
    class Point:
        def __init__(self, x):
            self.x = x

    assert list(it.pluck([{"x": 1}, Point(2)], "x")) == [1, 2]


def test_window_slides_over_sequence():
    assert list(it.window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]


def test_window_shorter_than_size_yields_nothing():
    assert list(it.window([1], 2)) == []


def test_inputs_are_not_mutated():
    data = [3, 1, 2, 1]
    list(it.unique(data))
    list(it.chunk(data, 2))
    assert data == [3, 1, 2, 1]
