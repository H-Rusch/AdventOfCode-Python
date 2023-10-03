from collections import Counter
import re


def part1(input: str) -> int:
    instructions = parse(input)

    turned_on = set()

    for instruction in instructions:
        op, x0, x1, y0, y1, z0, z1 = instruction[:]
        if any([abs(v) > 50 for v in instruction[1:]]):
            continue

        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    if op == "on":
                        turned_on.add((x, y, z))
                    else:
                        turned_on.discard((x, y, z))

    return len(turned_on)


# improved on /u/Boojum's solution because I did not want to fiddle with those coordinates anymore
def part2(input: str) -> int:
    instructions = parse(input)

    cubes = Counter()

    for instruction in instructions:
        op, new_x0, new_x1, new_y0, new_y1, new_z0, new_z1 = instruction
        new_sign = 1 if op == "on" else -1

        update = Counter()
        to_remove = []
        for (old_x0, old_x1, old_y0, old_y1, old_z0, old_z1), old_sign in cubes.items():
            # existing cube is fully enveloped into the new cube, so the existing cube is removed
            if old_x0 >= new_x0 and old_x1 <= new_x1 and \
                    old_y0 >= new_y0 and old_y1 <= new_y1 and \
                    old_z0 >= new_z0 and old_z1 <= new_z1:
                to_remove.append(
                    (old_x0, old_x1, old_y0, old_y1, old_z0, old_z1))
            else:
                # i := intersection
                i_x0 = max(new_x0, old_x0)
                i_x1 = min(new_x1, old_x1)
                i_y0 = max(new_y0, old_y0)
                i_y1 = min(new_y1, old_y1)
                i_z0 = max(new_z0, old_z0)
                i_z1 = min(new_z1, old_z1)

                if i_x0 <= i_x1 and i_y0 <= i_y1 and i_z0 <= i_z1:
                    update[(i_x0, i_x1, i_y0, i_y1, i_z0, i_z1)] -= old_sign

        if new_sign > 0:
            update[(new_x0, new_x1, new_y0, new_y1, new_z0, new_z1)] += new_sign

        for remove in to_remove:
            cubes.pop(remove)
        cubes.update(update)

        # remove cubes which value incremented/ decremented to 0
        to_remove.clear()
        for coordinate, value in cubes.items():
            if value == 0:
                to_remove.append(coordinate)
        for remove in to_remove:
            cubes.pop(remove)

    return sum((x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1) * sign for (x0, x1, y0, y1, z0, z1), sign in cubes.items())


def parse(input: str):
    instructions = []

    for line in input.splitlines():
        inst, x0, x1, y0, y1, z0, z1 = re.search(
            r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line).groups()
        instructions.append(
            (inst, int(x0), int(x1), int(y0), int(y1), int(z0), int(z1)))

    return instructions
