import re


# number-number char: string
regex = re.compile("(\d+)-(\d+)\s(\w):\s(\w+)")


def part1(input):
    correct = 0

    for line in input.splitlines():
        match = regex.match(line)
        if match:
            groups = match.groups()
            if groups[3].count(groups[2]) in range(int(groups[0]), int(groups[1]) + 1):
                correct += 1

    return correct


def part2(input):
    correct = 0

    for line in input.splitlines():
        match = regex.match(line)
        if match:
            groups = match.groups()
            if bool(groups[3][int(groups[0]) - 1] == groups[2]) ^ bool(
                groups[3][int(groups[1]) - 1] == groups[2]
            ):
                correct += 1

    return correct
