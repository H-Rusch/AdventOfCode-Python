import re
from collections import defaultdict, deque


def part1(input: str) -> int:
    pots, transitions = parse(input)
    start_length = len(pots)

    for _ in range(20):
        next_pots = []
        pots = "...." + pots + "...."

        for i in range(2, len(pots) - 2):
            part = pots[i - 2:i + 3]
            next_pots.append(transitions[part])

        pots = "".join(next_pots)

    return sum_pots(pots, start_length)


def part2(input: str) -> int:
    pots, transitions = parse(input)

    when, summed, growth = find_constant_growth(pots, transitions, len(pots))

    return summed + (50_000_000_000 - when) * growth


def sum_pots(pots: str, start_length: int) -> int:
    # calculate how many entries were added on each side in oder to properly calculate the pot numbers
    expansion = (len(pots) - start_length) // 2
    summed = 0

    for i, pot in enumerate(pots):
        if pot == "#":
            summed += (i - expansion)

    return summed


def find_constant_growth(pots: str, transitions: dict, start_length: int) -> tuple:
    # find the point in time, where the sum increased by the same rate a high amount of times
    changes = deque(maxlen=200)
    summed = sum_pots(pots, start_length)
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

        new_sum = sum_pots(pots, start_length)
        changes.append(new_sum - summed)
        summed = new_sum

        c += 1
        if len(changes) == changes.maxlen and changes.count(changes[0]) == len(changes):
            return c, new_sum, changes[0]


def parse(input):
    start, instructions = input.split("\n\n")
    start = start[start.index(":") + 2:]

    transitions = defaultdict(lambda: ".")
    for instr in instructions.splitlines():
        prerequisite, result = re.match("([.#]{5}) => ([.#])", instr).groups()
        transitions[prerequisite] = result

    return start, transitions
