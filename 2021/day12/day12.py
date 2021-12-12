from collections import defaultdict


def part_1(neighbours: dict) -> int:
    return search_paths(neighbours, "start")


def part_2(neighbours: dict) -> int:
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


def parse_input():
    with open("input.txt", "r") as file:
        neighbours = defaultdict(list)
        for line in file.read().splitlines():
            a, b = line.split("-")
            neighbours[a] += [b]
            neighbours[b] += [a]

        return neighbours


if __name__ == "__main__":
    neighbour_dict = parse_input()

    print(f"Part 1: There are a total of {part_1(neighbour_dict)} paths through the cave system if "
          "you only visit small caves once.")

    print(f"Part 2: There are a total of {part_2(neighbour_dict)} paths through the cave system if "
          "you can visit a single small cave twice.")
