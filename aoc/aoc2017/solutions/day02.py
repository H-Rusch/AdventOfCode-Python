from typing import List
from itertools import permutations


def part1(input):
    rows = parse(input)

    return sum(map(checksum, rows))


def part2(input):
    rows = parse(input)

    return sum(map(even_division, rows))


def checksum(row: List[int]) -> int:
    min_value, max_value = min(row), max(row)

    return abs(max_value - min_value)


def even_division(row: List[int]) -> int:
    for divident, divisor in permutations(row, 2):
        ok, val = test_quotient(divident, divisor)
        if ok:
            return int(val)


def test_quotient(divident: int, divisor: int) -> (bool, float):
    quotient = divident / divisor

    return (float(quotient).is_integer(), quotient)


def parse(input: str) -> List[List[int]]:
    return [[int(n) for n in line.split()] for line in input.splitlines()]
