def part1(input: str) -> int:
    down, right, (width, height) = parse(input)

    step = 1

    while True:
        new_down, new_right = set(), set()
        change = False

        # right moves first
        for x, y in right:
            x1 = (x + 1) % width
            if (x1, y) in right or (x1, y) in down:
                new_right.add((x, y))
            else:
                change = True
                new_right.add((x1, y))

        # down moves afterwards
        for x, y in down:
            y1 = (y + 1) % height
            if (x, y1) in new_right or (x, y1) in down:
                new_down.add((x, y))
            else:
                change = True
                new_down.add((x, y1))

        if not change:
            return step

        step += 1
        down = new_down
        right = new_right


def part2(_: str):
    return "No 2nd task to do ^_^"


def parse(input: str):
    down, right = set(), set()
    area = input.splitlines()
    width, height = len(area[0]), len(area)
    for y, line in enumerate(area):
        for x in range(len(line)):
            if line[x] == "v":
                down.add((x, y))
            elif line[x] == ">":
                right.add((x, y))

    return down, right, (width, height)
