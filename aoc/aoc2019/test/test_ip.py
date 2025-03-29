from aoc.aoc2019.intcode.ip import InstructionPointer


def test_incrementing_increases_value():
    ip = InstructionPointer()

    ip.increment(4)

    assert ip.value == 4


def test_incrementing_by_negative_decreases_value():
    ip = InstructionPointer()
    ip.value = 10

    ip.increment(-4)

    assert ip.value == 6


def test_jump_flag_set_after_jumping():
    ip = InstructionPointer()

    ip.jump(15)

    assert ip.value == 15
    assert ip.just_jumped


def test_increase_after_jump_blocks_increase():
    ip = InstructionPointer()
    ip.jump(15)

    ip.increment(1)

    assert ip.value == 15
    assert not ip.just_jumped
