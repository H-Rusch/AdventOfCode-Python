def bus_with_shortest_wait():
    earliest_time = int(bus_plan[0])
    timeslots = [[int(bus), 0] for bus in bus_plan[1].split(",") if bus != "x"]
    shortest_wait_index = 0
    shortest_wait = 1000000

    for i in range(len(timeslots)):
        base_time = timeslots[i][0]
        time = base_time
        while time < earliest_time:
            time += base_time
        timeslots[i][1] = time - earliest_time
        if timeslots[i][1] < shortest_wait:
            shortest_wait = timeslots[i][1]
            shortest_wait_index = i

    print("The answer for part 1 is: {}".format(timeslots[shortest_wait_index][0] * timeslots[shortest_wait_index][1]))


def part2():
    # establish CRS (Chinese Remainder Theorem) https://de.wikipedia.org/wiki/Chinesischer_Restsatz
    # search t so that t is the solution to: (=~ := congruent)
    # t =~ 0  (mod 19)
    # t =~ 9  (mod 41)
    # t =~ 19 (mod 643)
    # t =~ 36 (mod 17)
    # t =~ 37 (mod 13)
    # t =~ 42 (mod 23)
    # t =~ 50 (mod 509)
    # t =~ 56 (mod 37)
    # t =~ 79 (mod 29)
    bus_list = bus_plan[1].split(",")
    M = 1
    equations = [[i, int(bus_list[i])] for i in range(len(bus_list)) if bus_list[i] != "x"]
    for e in equations:
        M *= e[1]

    t = 0
    # for every equation calculate r_i * m_i + s_i * M_i = 1 where s_i comes from the eeA
    # set e_i to s_i * M_i
    # t is the sum of a_i * e_i
    for e in equations:
        M_i = M // e[1]
        # e_i := s_i * M_i
        e_i = extended_euclidian_algorithm(M_i, e[1])[0] * M_i
        t += e[0] * e_i

    print("\nThe answer for part 2 is: {}".format(M - (t % M)))


def extended_euclidian_algorithm(a: int, b: int):
    # entry of table: [r_j-1, q_j, r_j, r_j+1, x_j, y_j]
    table = [[None, None, a, b, 1, 0],
             [a, a // b, b, a % b, 0, 1]]
    j = 1
    while True:
        r_jm1 = table[j][2]
        r_j = table[j][3]
        q_j = r_jm1 // r_j
        r_jp1 = r_jm1 - r_j * q_j
        x_j = table[j - 1][4] - table[j][4] * table[j][1]
        y_j = table[j - 1][5] - table[j][5] * table[j][1]

        table.append([r_jm1, q_j, r_j, r_jp1, x_j, y_j])
        j += 1
        if r_jp1 == 0:
            break

    return [table[-1][4], table[-1][5]]


# read in bus plan
with open("input.txt", "r") as file:
    bus_plan = [direct for direct in file.read().split("\n")]

bus_with_shortest_wait()
part2()
extended_euclidian_algorithm(99, 78)
