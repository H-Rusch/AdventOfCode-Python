import functools


def part1(input: str) -> int:
    matrix = parse(input)
    points = get_low_points(matrix)

    return sum(map(lambda n: n + 1, [matrix[y][x] for (x, y) in points]))


def part2(input: str) -> int:
    matrix = parse(input)
    points = get_low_points(matrix)

    basin_areas = sorted(get_basin_sizes(points, matrix), reverse=True)[:3]

    return functools.reduce(lambda n1, n2: n1 * n2, basin_areas)


def get_low_points(matrix: list) -> list:
    points = []
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if all([matrix[y][x] < matrix[adj[1]][adj[0]] for adj in get_adjacent_coordinates(x, y, matrix)]):
                points.append((x, y))

    return points


def get_adjacent_coordinates(x: int, y: int, matrix: list) -> list:
    adjacent_coordinates = []
    if x > 0:
        adjacent_coordinates.append((x - 1, y))
    if x < len(matrix[0]) - 1:
        adjacent_coordinates.append((x + 1, y))

    if y > 0:
        adjacent_coordinates.append((x, y - 1))
    if y < len(matrix) - 1:
        adjacent_coordinates.append((x, y + 1))

    return adjacent_coordinates


def get_basin_sizes(point_list: list, matrix: list) -> list:
    """
    Start from low point and go towards the edges of the basin (The points with height 9).
    """
    basin_sizes = []
    for low_point in point_list:
        depths = []
        checked_coordinates = []
        coordinates_to_check = [(low_point[0], low_point[1])]

        while len(coordinates_to_check[:]) != 0:
            current = coordinates_to_check.pop(0)
            # add the depth of the current coordinate to the depths list
            depths.append(matrix[current[1]][current[0]])
            checked_coordinates.append(current)

            # get the neighbouring coordinates from the current coordinate and if they are flowing towards the low
            # point (i.e. they do not have a height of 9), they are added to the coordinates to check list.
            # also do not look at a coordinate which has already been looked at
            for coordinate in get_adjacent_coordinates(current[0], current[1], matrix):
                if matrix[coordinate[1]][coordinate[0]] != 9 and coordinate not in coordinates_to_check and \
                        coordinate not in checked_coordinates:
                    coordinates_to_check.append(coordinate)

        basin_sizes.append(len(depths))

    return basin_sizes


def parse(input: str):
    return [[int(n) for n in row] for row in input.splitlines()]
