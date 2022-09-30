from copy import deepcopy


def part_1(grid: list) -> int:
    for _ in range(10):
        grid = state_change(grid)

    return calc_score(get_state_string(grid))


def part_2(grid: list) -> int:
    history = [get_state_string(grid)]
    limit = 1_000_000_000
    for minute in range(1, limit + 1):
        grid = state_change(grid)
        letters = get_state_string(grid)

        if letters in history:
            repeat = history.index(letters)
            period = minute - repeat
            cycles = history[repeat:]

            return calc_score(cycles[(limit - repeat) % period])

        history.append(letters)

    letters = get_state_string(grid)
    return letters.count("|") * letters.count("#")


def calc_score(letters: str) -> int:
    return letters.count("|") * letters.count("#")


def state_change(grid: list) -> list:
    next_state = deepcopy(grid)

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            tree, free, lumber = count_adj_categories(grid, x, y)

            current = grid[y][x]
            if current == ".":
                next_state[y][x] = "|" if tree >= 3 else "."
            elif current == "|":
                next_state[y][x] = "#" if lumber >= 3 else "|"
            else:
                next_state[y][x] = "#" if lumber >= 1 and tree >= 1 else "."

    return next_state


def count_adj_categories(grid: list, x: int, y: int) -> tuple:
    counts = {"#": 0, ".": 0, "|": 0}

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            other_x, other_y = x + dx, y + dy
            if dy == dx == 0 or other_y < 0 or other_y >= len(grid) or other_x < 0 or other_x >= len(grid[other_y]):
                continue
            counts[grid[y + dy][x + dx]] += 1

    return counts["|"], counts["."], counts["#"]


def get_state_string(grid: list) -> str:
    return "".join(["".join([l for l in line]) for line in grid])


def parse_input():
    with open("input.txt", "r") as file:
        grid = [[l for l in line] for line in file.read().strip().splitlines()]

        return grid


if __name__ == "__main__":
    area_grid = parse_input()

    print(f"Part 1: The total resource value after 10 minutes is {part_1(area_grid)}.")

    print(f"Part 2: The total resouce value after 1 Billion minutes is {part_2(area_grid)}.")
