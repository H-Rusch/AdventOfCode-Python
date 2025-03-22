from aoc.util.direction import Direction


def test_direction_can_be_created_from_str():
    for dir in ["right", ">", "RIGHT", "r", "East"]:
        assert Direction.from_str(dir) == Direction.RIGHT
    for dir in ["up", "^", "UP", "u", "North"]:
        assert Direction.from_str(dir) == Direction.UP
    for dir in ["left", "<", "LEFT", "l", "West"]:
        assert Direction.from_str(dir) == Direction.LEFT
    for dir in ["down", "V", "DOWN", "d", "SOUTH"]:
        assert Direction.from_str(dir) == Direction.DOWN


def test_direction_from_str_returns_none_for_unknown_values():
    assert Direction.from_str("") is None
    assert Direction.from_str("weast") is None


def test_turn_right():
    assert Direction.RIGHT.turn_right() == Direction.DOWN
    assert Direction.DOWN.turn_right() == Direction.LEFT
    assert Direction.LEFT.turn_right() == Direction.UP
    assert Direction.UP.turn_right() == Direction.RIGHT


def test_turn_right_times():
    assert Direction.RIGHT.turn_right(0) == Direction.RIGHT
    assert Direction.RIGHT.turn_right(1) == Direction.DOWN
    assert Direction.RIGHT.turn_right(2) == Direction.LEFT
    assert Direction.RIGHT.turn_right(3) == Direction.UP
    assert Direction.RIGHT.turn_right(4) == Direction.RIGHT


def test_turn_left():
    assert Direction.RIGHT.turn_left() == Direction.UP
    assert Direction.DOWN.turn_left() == Direction.RIGHT
    assert Direction.LEFT.turn_left() == Direction.DOWN
    assert Direction.UP.turn_left() == Direction.LEFT


def test_turn_left_times():
    assert Direction.RIGHT.turn_left(0) == Direction.RIGHT
    assert Direction.RIGHT.turn_left(1) == Direction.UP
    assert Direction.RIGHT.turn_left(2) == Direction.LEFT
    assert Direction.RIGHT.turn_left(3) == Direction.DOWN
    assert Direction.RIGHT.turn_left(4) == Direction.RIGHT


def test_turn_around():
    assert Direction.RIGHT.turn_around() == Direction.LEFT
    assert Direction.LEFT.turn_around() == Direction.RIGHT
    assert Direction.DOWN.turn_around() == Direction.UP
    assert Direction.UP.turn_around() == Direction.DOWN


def test_steps():
    assert Direction.RIGHT.steps((1, 1)) == (2, 1)
    assert Direction.UP.steps((1, 1)) == (1, 0)
    assert Direction.LEFT.steps((1, 1)) == (0, 1)
    assert Direction.DOWN.steps((1, 1)) == (1, 2)
    assert Direction.RIGHT.steps((1, 1), 2) == (3, 1)
