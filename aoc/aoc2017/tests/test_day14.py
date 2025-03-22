from ..solutions import day14


def test_translation_to_binary():
    hashed = "a0c2017".ljust(32, "0")
    assert day14.convert_knot_hash_to_binary(hashed).startswith(
        "10100000110000100000000101110000"
    )


def test_part1_example():
    assert 8108 == day14.part1("flqrgnkx")


def test_part2_example():
    assert 1242 == day14.part2("flqrgnkx")
