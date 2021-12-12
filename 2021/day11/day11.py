def both_parts(octopus_dict: dict) -> tuple:
    steps = 0
    number_of_flashes = 0

    while True:
        flashing = set()
        flashed = set()
        # increment all octopuses by 1
        for coordinate in octopus_dict.keys():
            octopus_dict[coordinate] += 1
            if octopus_dict[coordinate] == 10:
                flashing.add(coordinate)

        # flash the flashing octopuses
        while len(flashing) != 0:
            coordinate = flashing.pop()
            for adjacent in get_adjacent(coordinate, octopus_dict):
                octopus_dict[adjacent] += 1
                if octopus_dict[adjacent] == 10:
                    flashing.add(adjacent)
            flashed.add(coordinate)

            # count the number of flashes up to step 100
            if steps < 100:
                number_of_flashes += 1

        # reset the value of the flashed octopuses
        for coordinate in flashed:
            octopus_dict[coordinate] = 0

        steps += 1

        if sum([octopus_dict[cord] for cord in octopus_dict.keys()]) == 0:
            break

    return number_of_flashes, steps


def get_adjacent(coordinate: tuple, octopus_dict: dict) -> list:
    adj = set([(coordinate[0] + x, coordinate[1] + y) for x in (-1, 0, 1) for y in (-1, 0, 1) if not (x == y == 0)])

    return list(set(octopus_dict.keys()).intersection(adj))


def parse_input():
    with open("input.txt", "r") as file:
        matrix = [[int(n) for n in line] for line in file.read().splitlines()]

        coordinate_dict = {}
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                coordinate_dict[(x, y)] = matrix[y][x]

        return coordinate_dict


if __name__ == "__main__":
    octopus_matrix = parse_input()

    num_flashes, synchronized_flash_step = both_parts(octopus_matrix)

    print(f"Part 1: There have been a total of {num_flashes} flashes.")

    print(f"Part 2: The first step during all octopuses flash is at step {synchronized_flash_step}.")
