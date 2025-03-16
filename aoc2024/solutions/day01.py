from typing import List, Tuple
from collections import Counter


def part1(input: str) -> int:
    list1, list2 = parse(input)

    list1.sort()
    list2.sort()

    return sum([abs(left - right) for left, right in zip(list1, list2)])


def part2(input: str) -> int:
    list1, list2 = parse(input)

    counts = Counter(list2)

    return sum([counts[num] * num for num in list1])


def parse(input: str) -> Tuple[List[int], List[int]]:
    list1 = []
    list2 = []
    for line in input.splitlines():
        first, second = line.split()
        list1.append(int(first))
        list2.append(int(second))

    return (list1, list2)
