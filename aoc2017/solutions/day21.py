import numpy as np
from typing import Generator


START = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])


def part1(input):
    transformations = parse(input)
    matrix = START

    for _ in range(5):
        matrix = iteration(transformations, matrix)

    return np.sum(matrix)


def part2(input):
    transformations = parse(input)
    matrix = START

    for _ in range(18):
        matrix = iteration(transformations, matrix)

    return np.sum(matrix)


def iteration(transformations: dict, matrix: np.array) -> np.array:
    broken = break_up(matrix)
    transformed = transform_broken(transformations, broken)
    return rearange_parts(transformed)


def break_up(matrix: np.array) -> list[np.array]:
    parts = parts_count(matrix)

    return [np.split(sub, parts, axis=1) for sub in np.split(matrix, parts)]


def parts_count(matrix: np.array) -> int:
    if len(matrix) % 2 == 0:
        return len(matrix) // 2
    if len(matrix) % 3 == 0:
        return len(matrix) // 3


def transform_broken(transformations: dict, broken: list[np.array]) -> list[np.array]:
    transformed = []
    for row in broken:
        transformed_row = []
        for matrix in row:
            new_matrix = transformations[key_from_matrix(matrix)]
            transformed_row.append(new_matrix)
        transformed.append(transformed_row)

    return transformed


def rearange_parts(transformed: list[np.array]) -> np.array:
    new_rows = []
    for row in transformed:
        new_rows.append(np.hstack(row))

    return np.vstack(new_rows)


def parse(input: str) -> dict:
    transformations = {}
    for rule in input.splitlines():
        state, result = rule.split(" => ")
        state = build_from_description(state)
        result = build_from_description(result)

        define_transformations(transformations, state, result)

    return transformations


def build_from_description(description: str) -> np.array:
    description = description.replace(".", "0").replace("#", "1")
    return np.array([[int(n) for n in row] for row in description.split("/")])


def define_transformations(transformations: dict, matrix: np.array, result: np.array):
    for rotated in matrix_rotations(matrix):
        transformations[key_from_matrix(rotated)] = result


def matrix_rotations(matrix: np.array) -> Generator[np.array, None, None]:
    yield np.transpose(matrix)
    matrix = np.rot90(matrix)
    yield matrix
    yield np.transpose(matrix)
    matrix = np.rot90(matrix)
    yield matrix
    yield np.transpose(matrix)
    matrix = np.rot90(matrix)
    yield matrix
    yield np.transpose(matrix)
    matrix = np.rot90(matrix)
    yield matrix


def key_from_matrix(matrix: np.array) -> bytes:
    return "".join(str(n) for n in matrix.reshape(-1))
