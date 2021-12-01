from functools import reduce


file = open("input.txt", "r")
geomap = [i for i in file.read().splitlines()]
file.close()

# 5 different slopes. Save the amount of trees encountered in this list
tree_count = [0 for _ in range(5)]
x = [0 for _ in range(5)]

map_width = len(geomap[0])

for i in range(len(geomap)):
    # Right 1, down 1.
    if geomap[i][x[0]] == "#":
        tree_count[0] += 1
    x[0] = (x[0] + 1) % map_width

    # Right 3, down 1.
    if geomap[i][x[1]] == "#":
        tree_count[1] += 1
    x[1] = (x[1] + 3) % map_width

    # Right 5, down 1.
    if geomap[i][x[2]] == "#":
        tree_count[2] += 1
    x[2] = (x[2] + 5) % map_width

    # Right 7, down 1.
    if geomap[i][x[3]] == "#":
        tree_count[3] += 1
    x[3] = (x[3] + 7) % map_width

    # Right 1, down 2.
    if i % 2 == 0:
        if geomap[i][x[4]] == "#":
            tree_count[4] += 1
        x[4] = (x[4] + 1) % map_width

print(tree_count)
print(reduce(lambda a, b: a * b, tree_count))



