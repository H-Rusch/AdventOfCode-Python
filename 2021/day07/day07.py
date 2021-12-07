import numpy as np


def part_1(position_list: list) -> int:
    median = int(np.median(position_list))
    return sum([abs(n - median) for n in position_list])


def part_2(position_list: list) -> int:
    sorted_list = sorted(position_list)

    return min(sum([cost(abs(sorted_list[j] - i)) for j in range(len(sorted_list))])
               for i in range(sorted_list[-1]))


def cost(distance: int) -> int:
    # compute gaussian sum
    return int((distance ** 2 + distance) / 2)


def parse_input():
    with open("input.txt", "r") as file:
        return [int(s) for s in file.read().split(",")]


if __name__ == "__main__":
    horizontal_positions = parse_input()

    print(f"Part 1: The sum of all fuel to be spent is {part_1(horizontal_positions)}.")

    print(f"Part 2: The sum of all fuel to be spent is {part_2(horizontal_positions)}.")
