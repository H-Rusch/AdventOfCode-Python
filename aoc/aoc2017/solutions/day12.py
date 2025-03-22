import re
from collections import deque
import random

PIPE_PATTERN = re.compile(r"(\d+) <-> (.*)")


def part1(input):
    pipes = parse(input)

    return len(expand_group(0, pipes))


def part2(input):
    pipes = parse(input)

    group_count = 0
    programs = pipes.keys()

    while len(programs) > 0:
        current = random.sample(sorted(programs), 1)[0]
        group = expand_group(current, pipes)
        programs -= group
        group_count += 1

    return group_count


def expand_group(start: int, pipes: dict) -> set[int]:
    visited = set()
    expanded = deque([start])

    while len(expanded) > 0:
        current = expanded.popleft()

        if current in visited:
            continue
        visited.add(current)

        expanded.extend(pipes[current])

    return visited


def parse(input) -> dict[str, list[str]]:
    pipes = {}

    for line in input.splitlines():
        program, connected_to = PIPE_PATTERN.match(line).groups()
        pipes[int(program)] = [int(num) for num in connected_to.split(", ")]

    return pipes
