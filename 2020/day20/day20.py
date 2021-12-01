def part1(fragments: list):
    # create a dictionary of the tiles when reading them in. The borders are stored as an entry
    fragment_dict = dict()
    for fragment in fragments:
        fragment_id = int(fragment[fragment.find(" ") + 1:fragment.find(":")])
        fragment_map = fragment[fragment.find("\n") + 1:].split("\n")
        top_edge = fragment_map[0]
        bottom_edge = fragment_map[-1]
        left_edge = "".join(line[0] for line in fragment_map)
        right_edge = "".join(line[-1] for line in fragment_map)

        fragment_dict[fragment_id] = [top_edge, bottom_edge, left_edge, right_edge]

    # find out how many neighbours there are for each tile. Corners only have 2 neighbours
    solution = 1
    for entry in fragment_dict.items():
        neighbours = 0
        for other_entry in fragment_dict.items():
            if other_entry[0] != entry[0]:
                for edge in entry[1]:
                    for i in range(4):
                        # compare the edge of the current entry to the edges of the other entries.
                        # Also check if it fits for a flipped edge
                        if edge == other_entry[1][i] or edge == "".join(list(reversed(other_entry[1][i]))):
                            neighbours += 1
        if neighbours == 2:
            solution *= entry[0]

    print(solution)


# read in map-fragments
with open("input.txt", "r") as file:
    fragment_list = [fragment for fragment in file.read().split("\n\n")]
    part1(fragment_list)
