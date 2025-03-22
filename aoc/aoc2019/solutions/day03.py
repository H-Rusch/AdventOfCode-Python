from collections import defaultdict


def part1(input) -> int:
    instructions = parse(input)

    line1 = get_coordinates(instructions[0])
    line2 = get_coordinates(instructions[1])

    intersections = line1.intersection(line2)

    # return minimum manhattan distance to origin
    return min([abs(c[0]) + abs(c[1]) for c in intersections])


def part2(input) -> int:
    instructions = parse(input)

    line1 = get_coordinates_and_steps(instructions[0])
    line2 = get_coordinates_and_steps(instructions[1])

    intersection = set(line1.keys()).intersection(set(line2.keys()))

    return min([line1[c] + line2[c] for c in intersection])


def get_coordinates(instructions: list) -> set:
    x, y = 0, 0
    coordinates = set()
    for instruction in instructions:
        for _ in range(int(instruction[1:])):
            if instruction.startswith("R"):
                x += 1
            elif instruction.startswith("U"):
                y -= 1
            elif instruction.startswith("L"):
                x -= 1
            else:
                y += 1
            coordinates.add((x, y))

    return coordinates


def get_coordinates_and_steps(instructions: list) -> dict:
    x, y, steps = 0, 0, 0
    coordinates = defaultdict(int)
    for instruction in instructions:
        for _ in range(int(instruction[1:])):
            if instruction.startswith("R"):
                x += 1
            elif instruction.startswith("U"):
                y -= 1
            elif instruction.startswith("L"):
                x -= 1
            else:
                y += 1
            steps += 1
            if (x, y) not in coordinates.keys():
                coordinates[(x, y)] = steps

    return coordinates


def parse(input):
    return [line.split(",") for line in input.splitlines()]
