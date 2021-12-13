import re


def part_1(coordinates: set, instruction_list: list) -> int:
    folded_coordinates = fold(coordinates, instruction_list[0])

    return len(folded_coordinates)


def part_2(coordinates: set, instruction_list: list):
    for i in range(len(instruction_list)):
        coordinates = fold(coordinates, instruction_list[i])

    show_coordinates(coordinates)


def fold(coordinates: set, instruction: str) -> set:
    direction, cutoff = re.search(r"([xy])=(\d+)", instruction).groups()
    cutoff = int(cutoff)

    folding_set = set()
    for coordinate in coordinates:
        x = coordinate[0]
        y = coordinate[1]

        if direction == "x" and x > cutoff:
            x = cutoff - abs(cutoff - x)
        elif direction == "y" and y > cutoff:
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


def parse_input():
    with open("input.txt", "r") as file:
        points, fold_instructions = file.read().split("\n\n")
        points = [point.split(",") for point in points.splitlines()]
        points = set([(int(point[0]), int(point[1])) for point in points])

        fold_instructions = fold_instructions.splitlines()

        return points, fold_instructions


if __name__ == "__main__":
    coordinate_set, instructions = parse_input()

    print(f"Part 1: After the first fold, there are {part_1(coordinate_set, instructions)} points visible.")

    print(f"Part 2: The final page in the instruction manual looks like this when folded:")
    part_2(coordinate_set, instructions)
