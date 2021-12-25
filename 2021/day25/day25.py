def part_1(down: set, right: set, size: tuple) -> int:
    step = 1
    width, height = size

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


def parse_input():
    with open("input.txt", "r") as file:
        down, right = set(), set()
        area = file.read().splitlines()
        width, height = len(area[0]), len(area)
        for y, line in enumerate(area):
            for x in range(len(line)):
                if line[x] == "v":
                    down.add((x, y))
                elif line[x] == ">":
                    right.add((x, y))

        return down, right, (width, height)


if __name__ == "__main__":
    down_population, right_population, dimension = parse_input()

    print(f"Part 1: The sea cucumbers stop moving after {part_1(down_population, right_population, dimension)} steps.")
