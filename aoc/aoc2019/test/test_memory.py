import pytest

from aoc.aoc2019.intcode.memory import Memory


def test_memory_copies_input_list():
    data = [1, 2, 3]
    memory = Memory(data)

    memory[1] = 4

    assert data[1] != memory[1]


def test_memory_raises_key_error_on_negative_index():
    memory = Memory([0])
    with pytest.raises(IndexError):
        memory[-1]
    with pytest.raises(IndexError):
        memory[-1] = 1


def test_accessing_valid_index_returns_correct_value():
    memory = Memory([1, 2, 3])

    assert memory[0] == 1
    assert memory[1] == 2
    assert memory[2] == 3


def test_slice_accessing_works():
    memory = Memory([1, 2, 3])

    assert memory[:1] == [1]
    assert memory[::-1] == [3, 2, 1]
    assert memory[1::-1] == [2, 1]
    assert memory[1:5] == [2, 3]


def test_accessing_unallocated_index_allocates_space_and_reeturns_default():
    memory = Memory([])

    assert memory[0] == 0
    assert len(memory) == 1
    assert memory[10] == 0
    assert len(memory) == 11
