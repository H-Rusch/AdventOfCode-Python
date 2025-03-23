import re


def part1(input: str) -> int:
    coordinates, instructions = parse(input)

    folded_coordinates = fold(coordinates, instructions[0])

    return len(folded_coordinates)


def part2(input: str):
    coordinates, instructions = parse(input)

    for i in range(len(instructions)):
        coordinates = fold(coordinates, instructions[i])

    show_coordinates(coordinates)


def fold(coordinates: set, instruction: str) -> set:
    axis, cutoff = re.search(r"([xy])=(\d+)", instruction).groups()
    cutoff = int(cutoff)

    folding_set = set()
    for coordinate in coordinates:
        x = coordinate[0]
        y = coordinate[1]

        if axis == "x" and x > cutoff:
            x = cutoff - abs(cutoff - x)
        elif axis == "y" and y > cutoff:
            y = cutoff - abs(cutoff - y)

        folding_set.add((x, y))

    return folding_set


def show_coordinates(coordinates: set):
    print_dict = {coordinate: "█ " for coordinate in coordinates}

    dimension_x = max([coordinate[0] for coordinate in coordinates])
    dimension_y = max([coordinate[1] for coordinate in coordinates])

    for y in range(dimension_y + 1):
        row = ""
        for x in range(dimension_x + 1):
            row += print_dict.get((x, y), "  ")
        print(row)


def parse(input: str):
    points, fold_instructions = input.split("\n\n")
    points = [point.split(",") for point in points.splitlines()]
    points = set([(int(point[0]), int(point[1])) for point in points])

    fold_instructions = fold_instructions.splitlines()

    return points, fold_instructions
