import math
from queue import PriorityQueue


def part_1(matrix: list) -> int:
    return get_shortest_path_risk_dijkstra(matrix)


def part_2(matrix: list) -> int:
    return get_shortest_path_risk_dijkstra(matrix)


def get_shortest_path_risk_dijkstra(matrix: list) -> int:
    # Dijkstra Algorithm
    limit = len(matrix) - 1
    end = (limit, limit)

    node_costs = {(x, y): math.inf for x in range(len(matrix)) for y in range(len(matrix))}

    expanded = PriorityQueue()
    expanded.put((0, (0, 0)))

    visited = set()

    while True:
        risk, current = expanded.get()

        if current == end:
            return risk

        visited.add(current)

        for neighbour in get_adjacent(current[0], current[1], limit):
            if neighbour not in visited:
                risk_summed = risk + matrix[neighbour[1]][neighbour[0]]

                if risk_summed < node_costs[neighbour]:
                    node_costs[neighbour] = risk_summed
                    expanded.put((risk_summed, neighbour))


def get_adjacent(x: int, y: int, limit: int) -> list:
    coordinates = []
    if x > 0:
        coordinates.append((x - 1, y))
    if x < limit:
        coordinates.append((x + 1, y))

    if y > 0:
        coordinates.append((x, y - 1))
    if y < limit:
        coordinates.append((x, y + 1))

    return coordinates


def parse_input():
    with open("input.txt", "r") as file:
        return [[int(n) for n in row] for row in file.read().splitlines()]


if __name__ == "__main__":
    riskmap = parse_input()

    print(f"Part 1: The shortest path from the top left to the bottom right has a combined risk factor of"
          f" {part_1(riskmap)}.")

    big_map = [[0 for i in range(len(riskmap * 5))] for j in range(len(riskmap) * 5)]

    for i in range(5):
        for j in range(5):
            increment = i + j

            for y in range(len(riskmap)):
                for x in range(len(riskmap)):
                    value = riskmap[y][x]

                    value += increment
                    if value > 9:
                        value -= 9

                    offset_y = j * len(riskmap)
                    offset_x = i * len(riskmap)

                    big_map[y + offset_y][x + offset_x] = value

    print(f"Part 2: The shortest path from the top left to the bottom right has a combined risk factor of"
          f" {part_2(big_map)}.")
