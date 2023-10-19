from ..solutions import day16


def test_spin():
    dance = day16.Dance(5)
    dance.spin(2)

    assert ["d", "e", "a", "b", "c"] == dance.programs


def test_exchange():
    dance = day16.Dance(5)
    dance.exchange(0, 3)

    assert ["d", "b", "c", "a", "e"] == dance.programs


def test_partner():
    dance = day16.Dance(5)
    dance.partner("b", "c")

    assert ["a", "c", "b", "d", "e"] == dance.programs
