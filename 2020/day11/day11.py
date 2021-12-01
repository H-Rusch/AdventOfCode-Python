def count_adjacent(i: int, j: int, seats):
    adjacent_count = 0
    # top row
    if i > 0:
        if j > 0 and seats[i - 1][j - 1] == "#":  # top left
            adjacent_count += 1
        if seats[i - 1][j] == "#":  # top
            adjacent_count += 1
        if j + 1 < len(seats[i]) and seats[i - 1][j + 1] == "#":  # top right
            adjacent_count += 1
    # same row
    if j > 0 and seats[i][j - 1] == "#":  # left
        adjacent_count += 1
    if j + 1 < len(seats[i]) and seats[i][j + 1] == "#":  # right
        adjacent_count += 1
    # bottom row
    if i + 1 < len(seats):
        if j > 0 and seats[i + 1][j - 1] == "#":  # bottom left
            adjacent_count += 1
        if seats[i + 1][j] == "#":  # bottom
            adjacent_count += 1
        if j + 1 < len(seats[i]) and seats[i + 1][j + 1] == "#":  # bottom right
            adjacent_count += 1

    return adjacent_count


def count_seen(i: int, j: int, seats):
    seen_count = 0
    k = 1
    # top left
    while i - k >= 0 and j - k >= 0:
        if seats[i - k][j - k] == "#":
            seen_count += 1
            break
        elif seats[i - k][j - k] == "L":
            break
        k += 1
    k = 1
    # top
    while i - k >= 0:
        if seats[i - k][j] == "#":
            seen_count += 1
            break
        elif seats[i - k][j] == "L":
            break
        k += 1
    k = 1
    # top right
    while i - k >= 0 and j + k < len(seats[i]):
        if seats[i - k][j + k] == "#":
            seen_count += 1
            break
        elif seats[i - k][j + k] == "L":
            break
        k += 1

    k = 1
    # left
    while j - k >= 0:
        if seats[i][j - k] == "#":
            seen_count += 1
            break
        elif seats[i][j - k] == "L":
            break
        k += 1
    k = 1
    # right
    while j + k < len(seats[i]):
        if seats[i][j + k] == "#":
            seen_count += 1
            break
        elif seats[i][j + k] == "L":
            break
        k += 1

    k = 1
    # bottom left
    while i + k < len(seats) and j - k >= 0:
        if seats[i + k][j - k] == "#":
            seen_count += 1
            break
        elif seats[i + k][j - k] == "L":
            break
        k += 1
    k = 1
    # bottom
    while i + k < len(seats):
        if seats[i + k][j] == "#":
            seen_count += 1
            break
        elif seats[i + k][j] == "L":
            break
        k += 1
    k = 1
    # bottom right
    while i + k < len(seats) and j + k < len(seats[i]):
        if seats[i + k][j + k] == "#":
            seen_count += 1
            break
        elif seats[i + k][j + k] == "L":
            break
        k += 1

    return seen_count


# read in seats
file = open("input.txt", "r")
seats = [[le for le in st] for st in file.read().split("\n")]
file.close()

# part 1
seats_before = "".join(["".join(line) for line in seats])
while True:
    # take a 'snapshot' of the seats since the rules are applied at the same time for all seats
    seats_copy = [[seats[x][y] for y in range(len(seats[0]))] for x in range(len(seats))]  # copy seats by value

    for i in range(len(seats_copy)):
        for j in range(len(seats_copy[i])):
            adjacent_count = count_adjacent(i, j, seats_copy)
            # rule 1: If no seat adjacent to the checked seat is occupied, it will become seated
            if seats_copy[i][j] == "L" and adjacent_count == 0:
                seats[i][j] = "#"
            # rule 2: If 4 or more adjacent seats are occupied it becomes empty again
            elif seats_copy[i][j] == "#" and adjacent_count >= 4:
                seats[i][j] = "L"

    # check if applying the rules brought any changes
    seats_after = "".join(["".join(line) for line in seats])
    if seats_before == seats_after:
        print(str(seats_after.count("#")) + " seats are occupied.")
        break
    else:
        seats_before = seats_after

# read in seats
with open("input.txt", "r") as file:
    seats = [[le for le in st] for st in file.read().split("\n")]


# part 2
seats_before = "".join(["".join(line) for line in seats])
while True:
    # take a 'snapshot' of the seats since the rules are applied at the same time for all seats
    seats_copy = [[seats[x][y] for y in range(len(seats[0]))] for x in range(len(seats))]  # copy seats by value

    for i in range(len(seats_copy)):
        for j in range(len(seats_copy[i])):
            seen_count = count_seen(i, j, seats_copy)
            # rule 1: If no seat seen to the checked seat is occupied, it will become seated
            if seats_copy[i][j] == "L" and seen_count == 0:
                seats[i][j] = "#"
            # rule 2: If 5 or more sen seats are occupied it becomes empty again
            elif seats_copy[i][j] == "#" and seen_count >= 5:
                seats[i][j] = "L"

    # check if applying the rules brought any changes
    seats_after = "".join(["".join(line) for line in seats])
    if seats_before == seats_after:
        print(str(seats_after.count("#")) + " seats are occupied.")

        break
    else:
        seats_before = seats_after
