import math
from collections import defaultdict, deque


def part_1(coordinate_dict: dict) -> int:
    return max(coordinate_dict.values())


def part_2(coordinate: tuple, coordinate_list: list) -> int:
    coordinate_list.remove(coordinate)

    enhanced_coordinates = coordinates_at_angle(coordinate[0], coordinate[1], coordinate_list)
    coordinate_queue = deque(sorted(enhanced_coordinates.keys(), reverse=True))

    for _ in range(199):
        shooting_at = coordinate_queue.popleft()
        enhanced_coordinates[shooting_at].pop(0)
        if len(enhanced_coordinates[shooting_at]) != 0:
            coordinate_queue.append(shooting_at)

    last_shot = enhanced_coordinates[coordinate_queue.popleft()].pop(0)
    return last_shot[0][0] * 100 + last_shot[0][1]


def number_of_visible_coordinates(x1: int, y1: int, coordinate_list: list) -> int:
    """
    Set (x1, x2) as (0, 0). Use atan2 to calculate the angle [-180, 180] to all other coordinates.
    The number of different angles is the number of visible asteroids, since when two asteroids have the same degree,
    one is in front of the other.
    """
    angles = {math.atan2(y2 - y1, x2 - x1) for (x2, y2) in coordinate_list}

    return len(angles)


def coordinates_at_angle(x1: int, y1: int, coordinate_list: list) -> dict:
    coordinate_dict = defaultdict(list)

    for x2, y2 in coordinate_list:
        # swap the parameters to 'rotate' the angles by 90° since we want to start facing up.
        angle = math.atan2(x2 - x1, y2 - y1)

        # sqrt( (x2-x1)^2 + (y2-y1)^2 )
        distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

        # append coordinate and distance to the entries for this angle. Then sort the entries based on their distance
        coordinate_dict[angle].append(((x2, y2), distance))
        coordinate_dict[angle] = list(sorted(coordinate_dict[angle], key=lambda entry: entry[1]))

    return coordinate_dict


def parse_input():
    with open("input.txt", "r") as file:
        asteroid_map = file.read().splitlines()
        coordinates = []
        for y in range(len(asteroid_map)):
            for x in range(len(asteroid_map[y])):
                if asteroid_map[y][x] == "#":
                    coordinates.append((x, y))

        return coordinates


if __name__ == "__main__":
    asteroid_coordinates = parse_input()

    visible_coordinates = {(x, y): number_of_visible_coordinates(x, y, asteroid_coordinates)
                           for (x, y) in asteroid_coordinates}

    print(f"Part 1: The best location to detect asteroids, detects {part_1(visible_coordinates)} asteroids.")

    # best_location = max(visible_coordinates, key=visible_coordinates.get)  # both work
    best_location = max(visible_coordinates, key=lambda key: visible_coordinates.get(key))

    print(f"Part 2: The 200th asteroid shot has a 'score' of {part_2(best_location, asteroid_coordinates)}.")
