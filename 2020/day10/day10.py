# read in adapters
with open("input.txt", "r") as file:
    adapters = [int(adap) for adap in file.read().split("\n")]

# part 1
# prepare the adapters
adapters.sort()
adapters.insert(0, 0)
adapters.append(adapters[-1] + 3)
# calculate the differences in jolt and increment their counters
differences = [0, 0, 0]
for i in range(1, len(adapters)):
    differences[adapters[i] - adapters[i - 1] - 1] += 1

print("The number of 1-jolt differences multiplied by the number of 3-jolt differences is: {0}".format(
    differences[0] * differences[2]))

# part 2
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

print("There are {0} possible ways to arrange the adapters.".format(possibilities[max(adapters)]))
