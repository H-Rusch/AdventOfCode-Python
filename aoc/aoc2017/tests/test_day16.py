from ..solutions import day16


def test_spin():
    dance = day16.Dance(5)
    dance.spin(2)

    assert dance.programs == ["d", "e", "a", "b", "c"]


def test_exchange():
    dance = day16.Dance(5)
    dance.exchange(0, 3)

    assert dance.programs == ["d", "b", "c", "a", "e"]


def test_partner():
    dance = day16.Dance(5)
    dance.partner("b", "c")

    assert dance.programs == ["a", "c", "b", "d", "e"]
