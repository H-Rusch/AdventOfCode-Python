import string


def part_1(polymer: str) -> int:
    return react_and_measure(polymer)


def part_2(polymer: str) -> int:
    return min([react_and_measure(polymer, l) for l in string.ascii_lowercase])


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


def parse_input():
    with open("input.txt", "r") as file:
        return file.read().strip()


if __name__ == "__main__":
    polymer_str = parse_input()

    print()
    print(f"Part 1: After fully reacting the polymer it has a length of {part_1(polymer_str)} units.")

    print(f"Part 2: The shortest polymer which can produced has a length of {part_2(polymer_str)} units.")
