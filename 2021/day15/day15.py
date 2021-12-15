import bisect


def part_1(matrix: list) -> int:
    return get_shortest_path_risk_faster(matrix)


def part_2(matrix: list) -> int:
    return get_shortest_path_risk_faster(matrix)


def get_shortest_path_risk_faster(matrix: list) -> int:
    # A*
    limit = len(matrix) - 1
    end = (limit, limit)

    open_list = [((0, 0), 0)]  # ((x, y), cost)
    closed_set = set()

    while True:
        open_list.sort(key=lambda t: t[1])

        coordinate, cost = open_list.pop(0)

        if coordinate == end:
            return cost

        closed_set.add(coordinate)

        for adjacent in get_adjacent(coordinate[0], coordinate[1], limit):
            summed_cost = cost + matrix[adjacent[1]][adjacent[0]]

            if adjacent not in closed_set and (adjacent, summed_cost) not in open_list:
                open_list.append((adjacent, summed_cost))


def get_shortest_path_risk_slow(matrix: list) -> int:
    # works, but it already takes ~30 seconds for part 1, so I'm just not going to try it for part 2
    limit = len(matrix) - 1
    end = (limit, limit)

    current, risk = (0, 0), 0

    expanded_nodes = []  # list maintaining ((x, y), summed_risk).
    history = set()
    node_costs = dict()

    while current != end:
        for adjacent in get_adjacent(current[0], current[1], limit):
            summed_risk = risk + matrix[adjacent[1]][adjacent[0]]

            # don't expand a node which is already expanded, or which has a worse risk then an already expanded one
            if (adjacent, summed_risk) in history and node_costs[adjacent] <= summed_risk:
                continue

            # insert into sorted list based on the summed risk
            history.add((adjacent, summed_risk))
            node_costs[adjacent] = summed_risk
            bisect.insort_left(expanded_nodes, (adjacent, summed_risk), key=lambda t: t[1])

        current, risk = expanded_nodes.pop(0)

    return risk


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

    # print(f"Part 1: The shortest path from the top left to the bottom right has a combined risk factor of"
    #      f" {part_1(riskmap)}.")

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
