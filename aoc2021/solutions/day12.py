from collections import defaultdict


def part1(input: str) -> int:
    neighbours = parse(input)

    return search_paths(neighbours, "start")


def part2(input: str) -> int:
    neighbours = parse(input)

    return search_paths(neighbours, "start", small_twice=True)


def search_paths(graph: dict, cave: str, visited: set = None, small_twice: bool = False):
    if visited is None:
        visited = set()

    if cave == "end":
        return 1

    visited.add(cave)

    paths_to_end = 0
    for neighbour in graph[cave]:
        if neighbour[0].islower():
            # visit a small cave for the first time
            if neighbour not in visited:
                paths_to_end += search_paths(graph, neighbour, visited.copy(), small_twice)

            # visit a small cave which has been visited before. Consumes the ability to visit a small cave twice
            elif small_twice and neighbour not in ("start", "end"):
                paths_to_end += search_paths(graph, neighbour, visited.copy(), False)

        else:
            paths_to_end += search_paths(graph, neighbour, visited.copy(), small_twice)

    return paths_to_end


def parse(input: str):
    neighbours = defaultdict(list)
    for line in input.splitlines():
        a, b = line.split("-")
        neighbours[a] += [b]
        neighbours[b] += [a]

    return neighbours
