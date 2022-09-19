import numpy as np


def part_1(coordinates: list) -> int:
    edges = get_grid_edges(coordinates)

    closest_dict = dict()
    # calculate closest coordinate for each coordinate on the grid
    for x in range(edges[0], edges[1] + 1):
        for y in range(edges[2], edges[3] + 1):
            distances = np.array([manhatten_distance(x, y, cx, cy) for (cx, cy) in coordinates])
            closest_dict[(x, y)] = np.argmin(distances)
            if len(np.where(distances == np.min(distances))[0]) > 1:
                closest_dict[(x, y)] = "."

    # Go through the given coordinates and clauclate the their area.
    # If one tile which is closest to the given coordinate is on the edge, that area is infinite.
    area_counts = np.zeros(len(coordinates))
    for i, (cx, cy) in enumerate(coordinates):
        area_counts[i] = calculate_area(i, closest_dict, edges)

    return int(np.max(area_counts))


def calculate_area(i: int, closest_dict: dict, edges: tuple) -> int:
    def check_on_map_edge(xx: int, yy: int) -> bool:
        return xx == edges[0] or xx == edges[1] or yy == edges[2] or yy == edges[3]

    area = 0
    for (x, y), closest in closest_dict.items():
        if closest == i:
            area += 1
            if check_on_map_edge(x, y):
                return 0

    return area


def get_grid_edges(coordinates: list) -> tuple:
    min_x = min([c[0] for c in coordinates])
    max_x = max([c[0] for c in coordinates])
    min_y = min([c[1] for c in coordinates])
    max_y = max([c[1] for c in coordinates])

    return min_x, max_x, min_y, max_y


def manhatten_distance(x: int, y: int, dx: int, dy: int) -> int:
    return abs(dx - x) + abs(dy - y)


def part_2(coordinates: list) -> int:
    limit = 10_000
    edges = get_grid_edges(coordinates)

    n = 0
    for x in range(edges[0], edges[1] + 1):
        for y in range(edges[2], edges[3] + 1):
            added_distances = sum([manhatten_distance(x, y, cx, cy) for cx, cy in coordinates])
            if added_distances < limit:
                n += 1

    return 0


def parse_input():
    with open("input.txt", "r") as file:
        coordinates = []
        for line in file.read().splitlines():
            x, y = line.split(", ")
            coordinates.append((int(x), int(y)))
        return coordinates


if __name__ == "__main__":
    coordiante_list = parse_input()

    print(f"Part 1: The size of the largest non infinite area is {part_1(coordiante_list)}.")

    print(f"Part 2: The size of the region containting all locations which have a total distance to all given "
          f"coordinates of less thatn the given value is {part_2(coordiante_list)}.")
