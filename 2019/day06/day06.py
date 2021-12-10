from collections import defaultdict


def part_1(orbit_dict: dict) -> int:
    return sum([len(body_orbits_bodies(body, orbit_dict)) for body in orbit_dict.keys()])


def body_orbits_bodies(body: str, orbit_dict: dict) -> list:
    body_list = []
    orbiting = orbit_dict.get(body)
    while orbiting is not None:
        body_list.append(orbiting)
        orbiting = orbit_dict.get(orbiting)

    return body_list


def part_2(orbit_dict: dict) -> int:
    start = orbit_dict.get("YOU")
    target = orbit_dict.get("SAN")

    start_orbits = body_orbits_bodies(start, orbit_dict)
    target_orbits = body_orbits_bodies(target, orbit_dict)

    # Find bodies which 'YOU' and 'SAN' orbit around, so a path between 'YOU' and 'SAN' can be created. The number of
    # transfers to get to that body from 'YOU' is added with the number of transfers to get from that body to 'SAN'
    numbers_of_transfers = []
    for i in range(len(start_orbits)):
        if start_orbits[i] in target_orbits:
            numbers_of_transfers.append(i + target_orbits.index(start_orbits[i]) + 2)

    return min(numbers_of_transfers)


def parse_input():
    # return dictionary with entries 'A': 'B' which means 'A' orbits around 'B'
    orbit_dict = defaultdict(None)
    with open("input.txt", "r") as file:
        for line in file.read().splitlines():
            orbit_dict[line[line.find(")") + 1:]] = line[:line.find(")")]

    return orbit_dict


if __name__ == "__main__":
    orbits = parse_input()

    print(f"Part 1: The sum of direct and indirect orbits is {part_1(orbits)}.")

    print(f"Part 2: The minimum number of transfers to get to the body Santa orbits around is {part_2(orbits)}.")
