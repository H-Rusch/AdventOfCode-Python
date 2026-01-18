from ..solutions import day17


def test_spinlock_works():
    spinlock = day17.Spinlock(3)
    assert spinlock.numbers == [0]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 1]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 2, 1]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 2, 3, 1]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 2, 4, 3, 1]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 5, 2, 4, 3, 1]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 5, 2, 4, 3, 6, 1]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 5, 7, 2, 4, 3, 6, 1]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 5, 7, 2, 4, 3, 8, 6, 1]

    spinlock.insert_next()
    assert spinlock.numbers == [0, 9, 5, 7, 2, 4, 3, 8, 6, 1]


def test_part1_example():
    spinlock = day17.Spinlock(3)

    assert day17.execute_part1(spinlock) == 638
