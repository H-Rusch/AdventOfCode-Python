def part1(active: list):
    for _ in range(6):
        active_copy = set()

        x_values = [c[0] for c in active]
        y_values = [c[1] for c in active]
        z_values = [c[2] for c in active]

        # go through every existing coordinate and through the ones right next to those
        # min -1 and max + 1 -> expansion outwards
        for x in range(min(x_values) - 1, max(x_values) + 2):
            for y in range(min(y_values) - 1, max(y_values) + 2):
                for z in range(min(z_values) - 1, max(z_values) + 2):
                    # count the active neighbours by looking at every adjacent coordinate
                    neighbour_count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dz in [-1, 0, 1]:
                                # don't check the same cube as its own neighbour
                                if not (dx == 0 and dy == 0 and dz == 0):
                                    if (x + dx, y + dy, z + dz) in active:
                                        neighbour_count += 1
                    # keep a cube active or activate an inactive cube based on the given rules
                    if (x, y, z) in active and neighbour_count in [2, 3]:
                        active_copy.add((x, y, z))
                    if (x, y, z) not in active and neighbour_count == 3:
                        active_copy.add((x, y, z))
        active = active_copy

    return len(active)


def part2(active: list):
    for _ in range(6):
        active_copy = set()

        x_values = [c[0] for c in active]
        y_values = [c[1] for c in active]
        z_values = [c[2] for c in active]
        w_values = [c[3] for c in active]

        # go through every existing coordinate and through the ones right next to those
        # min -1 and max + 1 -> expansion outwards
        for x in range(min(x_values) - 1, max(x_values) + 2):
            for y in range(min(y_values) - 1, max(y_values) + 2):
                for z in range(min(z_values) - 1, max(z_values) + 2):
                    for w in range(min(w_values) - 1, max(w_values) + 2):
                        # count the active neighbours by looking at every adjacent coordinate
                        neighbour_count = 0
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                for dz in [-1, 0, 1]:
                                    for dw in [-1, 0, 1]:
                                        # don't check the same cube as it's own neighbour
                                        if not (dx == 0 and dy == 0 and dz == 0 and dw == 0):
                                            if (x + dx, y + dy, z + dz, w + dw) in active:
                                                neighbour_count += 1
                        # keep a cube active or activate an inactive cube based on the given rules
                        if (x, y, z, w) in active and neighbour_count in [2, 3]:
                            active_copy.add((x, y, z, w))
                        if (x, y, z, w) not in active and neighbour_count == 3:
                            active_copy.add((x, y, z, w))
        active = active_copy

    return len(active)


# read in beginning configuration
with open("input.txt", "r") as file:
    config = [direct for direct in file.read().split("\n")]

# read in as 3 dimensional coordinates for part 1
active = []
for x in range(len(config)):
    for y in range(len(config[x])):
        if config[x][y] == "#":
            active.append((x, y, 0))

print(f"Number of active cubes in Part 1 is: {part1(active)}")

# read in as 4 dimensional coordinates for part 2
active = []
for x in range(len(config)):
    for y in range(len(config[x])):
        if config[x][y] == "#":
            active.append((x, y, 0, 0))

print(f"Number of active cubes in Part 2 is: {part2(active)}")
