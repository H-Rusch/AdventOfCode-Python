import re

MUL_PATTERN = r"mul\((\d+),(\d+)\)"
DO_PATTERN = r"(do\(\))|(don't\(\))|mul\((\d+),(\d+)\)"


def part1(input: str) -> int:
    return sum(
        [int(val1) * int(val2) for (val1, val2) in re.findall(MUL_PATTERN, input)]
    )


def part2(input: str) -> int:
    enabled = True
    result = 0
    for do, dont, val1, val2 in re.findall(DO_PATTERN, input):
        if do:
            enabled = True
        elif dont:
            enabled = False
        elif enabled:
            result += int(val1) * int(val2)

    return result
