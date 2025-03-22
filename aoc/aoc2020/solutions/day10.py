def part1(input):
    adapters = parse(input)
    fill_adapters(adapters)

    # calculate the differences in jolt and increment their counters
    differences = [0, 0, 0]
    for i in range(1, len(adapters)):
        differences[adapters[i] - adapters[i - 1] - 1] += 1

    return differences[0] * differences[2]


def part2(input):
    adapters = parse(input)
    fill_adapters(adapters)

    # create dictionary which shows for each adapter how many ways there are to get to it.
    # Initially there is 1 way to get to the adapter 0
    adapters.pop()
    possibilities = {adap: 0 for adap in adapters}
    possibilities[0] = 1
    # check for each adapter [i] the next 3 adapters [i + j]. If those [i + j] can be reached the number of paths leading
    # to those adapters [i + j] is increased by the number of paths leading to the starting adapter [i].
    for i in range(len(adapters)):
        j = 1
        while i + j < len(adapters) and j < 4:  # check the next 3 elements
            if adapters[i + j] - adapters[i] <= 3:
                possibilities[adapters[i + j]] += possibilities[adapters[i]]
            j += 1

    return possibilities[max(adapters)]


def fill_adapters(adapters):
    adapters.sort()
    adapters.insert(0, 0)
    adapters.append(adapters[-1] + 3)


def parse(input):
    return [int(adap) for adap in input.splitlines()]
