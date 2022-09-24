import re
from collections import defaultdict, deque


def part_1(pots: str, transitions: dict) -> int:
    for _ in range(20):
        next_pots = []
        pots = "...." + pots + "...."

        for i in range(2, len(pots) - 2):
            part = pots[i - 2:i + 3]
            next_pots.append(transitions[part])

        pots = "".join(next_pots)

    return sum_pots(pots)


def sum_pots(pots: str) -> int:
    # calculate how many entries were added on each side in oder to properly calculate the pot numbers
    expansion = (len(pots) - start_length) // 2
    summed = 0

    for i, pot in enumerate(pots):
        if pot == "#":
            summed += (i - expansion)

    return summed


def part_2(pots: str, transitions: dict) -> int:
    when, summed, growth = find_constant_growth(pots, transitions)

    return summed + (50_000_000_000 - when) * growth


def find_constant_growth(pots: str, transitions: dict) -> tuple:
    # find the point in time, where the sum increased by the same rate a high amount of times
    changes = deque(maxlen=200)
    summed = sum_pots(pots)
    c = 0
    while True:
        # --- same as part 1
        next_pots = []
        pots = "...." + pots + "...."
        for i in range(2, len(pots) - 2):
            part = pots[i - 2:i + 3]
            next_pots.append(transitions[part])
        pots = "".join(next_pots)
        # --- same as part 1

        new_sum = sum_pots(pots)
        changes.append(new_sum - summed)
        summed = new_sum

        c += 1
        if len(changes) == changes.maxlen and changes.count(changes[0]) == len(changes):
            return c, new_sum, changes[0]


def parse_input():
    with open("input.txt", "r") as file:
        start, instructions = file.read().split("\n\n")
        start = start[start.index(":") + 2:]

        transitions = defaultdict(lambda: ".")
        for instr in instructions.splitlines():
            prerequisite, result = re.match("([.#]{5}) => ([.#])", instr).groups()
            transitions[prerequisite] = result

        return start, transitions


if __name__ == "__main__":
    pots_start, transition_dict = parse_input()
    start_length = len(pots_start)

    print(f"Part 1: The sum of the pot's numbers which have flowers in them after 20 iterations is " +
          f"{part_1(pots_start, transition_dict)}.")

    print(f"Part 2: The sum of the pot's numbers which have flowers in them after 50 Billion iterations is " +
          f"{part_2(pots_start, transition_dict)}.")
