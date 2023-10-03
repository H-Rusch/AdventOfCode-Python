from collections import defaultdict


def part1(bugs: set) -> int:
    past_positions = set(unique_repr(bugs))

    while True:
        new_bugs = set()
        for y in range(5):
            for x in range(5):
                count = count_adjacent_1(bugs, x, y)
                if (x, y) in bugs:
                    if count == 1:
                        new_bugs.add((x, y))
                else:
                    if count in [1, 2]:
                        new_bugs.add((x, y))
        bugs = new_bugs

        unique = unique_repr(bugs)
        if unique in past_positions:
            return calculate_biodiversity(bugs)
        else:
            past_positions.add(unique)


def part2(bugs: set) -> int:
    level_dict = defaultdict(set)
    level_dict[0] = bugs

    for _ in range(200):
        next_level_dict = defaultdict(set)
        for i in range(min(level_dict) - 1, max(level_dict) + 2):
            for y in range(5):
                for x in range(5):
                    count = count_adjacent_2(level_dict, x, y, i)
                    if (x, y) in level_dict[i]:
                        if count == 1:
                            next_level_dict[i].add((x, y))
                    else:
                        if (x, y) != (2, 2) and count in [1, 2]:
                            next_level_dict[i].add((x, y))

        level_dict = next_level_dict

    return sum(map(lambda d: len(d), level_dict.values()))


def count_adjacent_2(grids: dict, x: int, y: int, level: int) -> int:
    count = 0
    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_x, new_y = x + dx, y + dy
        if new_x == new_y == 2:
            # adjacent is middle of the grid -> go one level deeper
            other_level = grids[level + 1]
            if x == 2:
                if y < 2:
                    count += len([1 for i in range(5) if (i, 0) in other_level])
                else:
                    count += len([1 for i in range(5) if (i, 4) in other_level])
            elif y == 2:
                if x < 2:
                    count += len([1 for i in range(5) if (0, i) in other_level])
                else:
                    count += len([1 for i in range(5) if (4, i) in other_level])

        elif new_x < 0 or new_x > 4 or new_y < 0 or new_y > 4:
            # adjacent is outside the own grid -> go one level higher
            other_level = grids[level - 1]
            if new_x < 0:
                count += (1, 2) in other_level
            if new_x > 4:
                count += (3, 2) in other_level
            if new_y < 0:
                count += (2, 1) in other_level
            if new_y > 4:
                count += (2, 3) in other_level
        else:
            # adjacent is in the same grid
            count += (new_x, new_y) in grids[level]

    return count


def count_adjacent_1(bugs: set, x: int, y: int) -> int:
    count = 0
    for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if (x + dx, y + dy) in bugs:
            count += 1

    return count


def calculate_biodiversity(bugs: set) -> int:
    score = 0
    value = 1

    for y in range(5):
        for x in range(5):
            if (x, y) in bugs:
                score += value
            value *= 2

    return score


def unique_repr(bugs: set) -> str:
    return "".join([str(t) for t in sorted(list(bugs))])


def parse(input):
    with open("input.txt", "r") as file:
        lines = file.readlines()

        return {(x, y) for y in range(len(lines)) for x in range(len(lines[y])) if lines[y][x] == "#"}


if __name__ == "__main__":
    bug_positions = parse(input)

    print(f"Part 1: The biodiversity score of the first repeating pattern is {part1(bug_positions)}.")

    print(f"Part 2: After 200 minutes there are {part2(bug_positions)} bugs present.")
