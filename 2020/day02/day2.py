import re


file = open("input.txt", "r")
input = [i for i in file.read().splitlines()]
file.close()

# number-number char: string
regex = re.compile("(\d+)-(\d+)\s(\w):\s(\w+)")

correct1 = 0
correct2 = 0

for l in input:
    # [lower, upper, letter, password]
    match = regex.match(l)
    if match:
        groups = match.groups()
        # part 1
        if groups[3].count(groups[2]) in range(int(groups[0]), int(groups[1]) + 1):
            correct1 += 1

        # part 2
        # taking xor of booleans by making sure they are not equal
        if bool(groups[3][int(groups[0]) - 1] == groups[2]) ^ bool(groups[3][int(groups[1]) - 1] == groups[2]):
            correct2 += 1

print(correct1)
print(correct2)


