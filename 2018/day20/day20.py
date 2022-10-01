from collections import deque, defaultdict
import math


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


def part_1(distances: dict) -> int:
    return max(distances.values())


def part_2(distances: dict) -> int:
    return sum(distance >= 1000 for _, distance in distances.items())


def parse_input():
    with open("input.txt", "r") as file:
        return file.read().strip()[1:-1]


if __name__ == "__main__":
    regex_string = parse_input()
    distances_dict = build_facility(regex_string)

    print(f"Part 1: The largest number of doors required to reach a room on the shortest path is {part_1(distances_dict)}.")

    print(f"Part 2: The number of rooms that require at least 1000 doors to get to is {part_2(distances_dict)}.")
