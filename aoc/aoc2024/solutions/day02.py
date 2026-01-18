from itertools import pairwise


def part1(input: str) -> int:
    return len([report for report in parse(input) if is_safe(report)])


def part2(input: str) -> int:
    return len([report for report in parse(input) if can_be_safe(report)])


def is_safe(report: tuple[int]) -> bool:
    def is_steady() -> bool:
        return len({left < right for left, right in pairwise(report)}) == 1

    def are_differences_ok() -> bool:
        return all(abs(right - left) in range(1, 4) for left, right in pairwise(report))

    return is_steady() and are_differences_ok()


def can_be_safe(report: tuple[int]) -> bool:
    if is_safe(report):
        return True

    # generate is_safe for all 'subtuples' resulting from removing any 1 value from the original tuple
    return any(is_safe(tuple(report[:i] + report[i + 1 :])) for i in range(len(report)))


def parse(input: str) -> list[tuple[int]]:
    return [tuple([int(num) for num in line.split()]) for line in input.splitlines()]
