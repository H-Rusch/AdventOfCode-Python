import re

# read in docking parameters
with open("input.txt", "r") as file:
    docking_parameters = [parameter for parameter in file.read().split("\n")]

memory = dict()
mask = []

address_regex = re.compile(r"mem\[(\d*)] = (\d*)")

for parameter in docking_parameters:
    if parameter.startswith("mask = "):
        mask = list(parameter[7:])
    else:
        match = address_regex.search(parameter).groups()
        value = list(bin(int(match[1]))[2:].zfill(36))
        for i in range(len(mask)):
            if mask[i] == "1":
                value[i] = "1"
            elif mask[i] == "0":
                value[i] = "0"
        value = int("".join(value), 2)
        memory[match[0]] = value

print("The sum of values lef is: {}".format(sum(memory.values())))
