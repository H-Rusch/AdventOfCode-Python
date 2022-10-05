from collections import deque
from dataclasses import dataclass
from copy import deepcopy

# this one was no fun at all

@dataclass
class Unit:
    team: int
    pos: tuple
    hp: int = 200
    attack: int = 3
    alive: bool = True

    def do_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False


def part_1(grid: list, units: list) -> int:
    return fight(deepcopy(grid), deepcopy(units))[1]


def part_2(grid: list, units: list) -> int:
    boost = 11
    while True:
        all_elfs_alive, score = fight(deepcopy(grid), deepcopy(units), True, boost)
        if all_elfs_alive:
            return score
        boost += 1


def fight(grid: list, units: list, elfs_cant_die: bool = False, boost: int = 0) -> tuple:
    for unit in units:
        if unit.team == 0:
            unit.attack += boost

    round_count = 0
    while True:
        # print_grid(grid, units)
        # all units act in reading order
        units = sorted(units, key=lambda u: to_reading_order(u))
        killed = []

        # round
        for unit in units:
            if not unit.alive:
                continue
            target_positions = [target.pos for target in identifiy_targets(units, unit)]
            # no more enemies
            if len(target_positions) == 0:
                return True, calc_score(round_count, units)

            target = get_adjacent_target(grid, unit, units)
            if target is None:
                # move if not next to a pootential target
                next_to_target = {adj_to_target for target_x, target_y in target_positions
                                  for adj_to_target in get_adjacent(grid, target_x, target_y)}
                blocked = {u.pos for u in units if u.alive}
                next_to_target = next_to_target.difference(blocked)

                best_moves = list(bfs(grid, units, unit.pos, next_to_target))
                # cannot get to any target
                if len(best_moves) == 0:
                    continue

                to_move = where_to_move(best_moves)
                if to_move not in blocked:
                    unit.pos = to_move
                target = get_adjacent_target(grid, unit, units)

            # look for adjacent target again and now try to attack
            if target is not None:
                # attack target which is next to unit
                target.do_damage(unit.attack)

                # kill target
                if not target.alive:
                    if elfs_cant_die and target.team == 0:
                        return False, 0
                    killed.append(target)

        round_count += 1
        # removed killed targets
        for unit in killed:
            units.remove(unit)


def bfs(grid: list, units: list, start_pos: tuple, targets: set) -> list:
    solutions, min_steps = [], None

    blocked = {u.pos for u in units if u.alive}
    starting = [pos for pos in get_adjacent(grid, *start_pos) if pos not in blocked]

    for starting_adj in starting:
        expanded = deque([(1, starting_adj, starting_adj)])
        visited = set()
        while len(expanded) > 0:
            step, pos, first_pos = expanded.popleft()
            # already visited
            if pos in visited:
                continue
            visited.add(pos)

            # no longer set to find a shortest path
            if min_steps is not None and step > min_steps:
                break

            # add to list of solutions
            if pos in targets:
                if min_steps is None:
                    min_steps = step
                if step <= min_steps:
                    solutions.append((pos, step, first_pos))

            # go to unblocked adjacent position
            for other_pos in get_adjacent(grid, pos[0], pos[1]):
                if other_pos not in visited and other_pos not in blocked:
                    expanded.append((step + 1, other_pos, first_pos))

    if len(solutions) == 0:
        return []

    min_steps = min(map(lambda t: t[1], solutions))
    return [(pos, steps, first_pos) for (pos, steps, first_pos) in solutions if steps == min_steps]


def where_to_move(best_moves: list) -> tuple:
    # sort shortest path and reading order
    best_moves = sorted(best_moves, key=lambda bm: (bm[1], bm[0][1], bm[0][0]))
    # filter found solutions to only those which lead to selected position
    best_moves = [triple for triple in best_moves if triple[0] == best_moves[0][0]]
    # sort in read order offirst step
    best_moves = sorted(best_moves, key=lambda bm: (bm[2][1], bm[2][0]))

    return best_moves[0][2]


def calc_score(rounds: int, units: list) -> int:
    return rounds * sum(map(lambda u: u.hp, [u for u in units if u.alive]))


def get_adjacent_target(grid: list, unit: Unit, units: list) -> Unit:
    adj = get_adjacent(grid, unit.pos[0], unit.pos[1])
    adjacent_units = sorted([u for u in units if u.pos in adj and u.alive and u.team != unit.team],
                            key=lambda u: u.hp)

    if len(adjacent_units) > 0:
        return adjacent_units[0]


def get_adjacent(grid: list, x: int, y: int) -> list:
    adjacent = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        other_x, other_y = (x + dx, y + dy)
        if grid[other_y][other_x] == ".":
            adjacent.append((other_x, other_y))

    return adjacent


def identifiy_targets(units: list, attacker: Unit) -> list:
    return [u for u in units if u.team != attacker.team and u is not attacker and u.alive]


def to_reading_order(u: Unit) -> tuple:
    return u.pos[1], u.pos[0]


def to_reading_order_tuple(pos: tuple) -> tuple:
    return pos[1], pos[0]


def print_grid(grid: list, units: list):
    positions = {u.pos: u for u in units}
    for y, line in enumerate(grid):
        s = []
        e = []
        for x, sign in enumerate(line):
            if (x, y) in positions and positions[(x, y)].alive:
                a = "G" if positions[(x, y)].team == 1 else "E"
                s.append(a)
                e.append(str(positions[(x, y)].hp))
            else:
                s.append(grid[y][x])

        print(" ".join(s))  # , "  ".join(e))


def parse_input():
    with open("input.txt", "r") as file:
        data = file.read().strip()
        grid = [list(line) for line in data.splitlines()]
        units = []
        for y, line in enumerate(data.splitlines()):
            for x, sign in enumerate(line):
                if sign in {"G", "E"}:
                    team = 1 if sign == "G" else 0
                    units.append(Unit(team, (x, y)))
                    grid[y][x] = "."
                else:
                    grid[y][x] = sign

        return grid, units


if __name__ == "__main__":
    grid_dict, unit_list = parse_input()

    print(f"Part 1: {part_1(grid_dict, unit_list)}.")

    grid_dict, unit_list = parse_input()

    print(f"Part 2: {part_2(grid_dict, unit_list)}.")
