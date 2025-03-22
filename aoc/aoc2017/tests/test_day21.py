from ..solutions import day21
import numpy as np

EXAMPLE_INPUT = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""


def test_transformations():
    transformations = day21.parse(EXAMPLE_INPUT)
    # first example transformation
    expected = np.array([[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]])

    output = day21.iteration(transformations, day21.START)

    assert np.array_equal(expected, output)

    # second example transformation
    expected = np.array(
        [
            [1, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
    )

    output = day21.iteration(transformations, output)

    assert np.array_equal(expected, output)
