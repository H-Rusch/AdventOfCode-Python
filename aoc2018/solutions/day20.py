from collections import deque, defaultdict
import math


def part1(input: str) -> int:
    regex_string = parse(input)
    distances = build_facility(regex_string)

    return max(distances.values())


def part2(input: str) -> int:
    regex_string = parse(input)
    distances = build_facility(regex_string)

    return sum(distance >= 1000 for _, distance in distances.items())


def build_facility(regex: str) -> dict:
    distances = defaultdict(lambda: math.inf)
    distance = 0
    coordinate = 0 + 0j
    stack = deque()

    for letter in regex:
        moves = {"N": 0 + 1j, "W": -1 + 0j, "S": 0 - 1j, "E": 1 + 0j}

        if letter == "(":
            stack.append((coordinate, distance))
        elif letter == ")":
            coordinate, distance = stack.pop()
        elif letter == "|":
            coordinate, distance = stack[-1]
        else:
            coordinate += moves[letter]
            distance += 1
            distances[coordinate] = int(min(distance, distances[coordinate]))

    return distances


def parse(input):
    return input.strip()[1:-1]
