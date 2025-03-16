import string


def part1(polymer: str) -> int:
    return react_and_measure(polymer)


def part2(polymer: str) -> int:
    return min([react_and_measure(polymer, ch) for ch in string.ascii_lowercase])


def react_and_measure(polymer: str, ignore: str = None) -> int:
    stack = []
    for c in polymer:
        # ignoring specific letters instead of removing them for part 2
        if ignore is not None and c.lower() == ignore:
            continue

        if len(stack) > 0 and c == stack[-1].swapcase():
            stack.pop()
        else:
            stack.append(c)

    return len(stack)
