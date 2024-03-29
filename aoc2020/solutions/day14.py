import re


def part1(input) -> int:
    mask = ""
    memory = dict()

    for instruction in input.splitlines():
        if instruction.startswith("mask"):
            mask = instruction[7:]
        else:
            address, value = re.search(r"mem\[(\d+)] = (\d+)", instruction).groups()
            value = list(bin(int(value))[2:].zfill(36))
            for i, b in enumerate(value):
                if mask[i] == "1":
                    value[i] = "1"
                elif mask[i] == "0":
                    value[i] = "0"
            memory[address] = int("".join(value), 2)

    return sum(memory.values())


def part2(input) -> int:
    mask = ""
    memory = dict()

    for instruction in input.splitlines():
        if instruction.startswith("mask"):
            mask = instruction[7:]
        else:
            address, value = re.search(r"mem\[(\d+)] = (\d+)", instruction).groups()

            address = list(bin(int(address))[2:].zfill(36))
            for possible_address in get_floating_addresses(address, mask):
                memory[possible_address] = int(value)

    return sum(memory.values())


def get_floating_addresses(address: list, mask: str):
    expanded = [(address, 0)]
    finished = []
    while len(expanded) > 0:
        current, i = expanded.pop()

        while i < len(current):
            if mask[i] == "1":
                current[i] = "1"
                i += 1
            elif mask[i] == "0":
                current[i] = current[i]
                i += 1
            else:
                if i == 0:
                    replace_0 = ["0"] + current[i + 1 :]
                    replace_1 = ["1"] + current[i + 1 :]

                elif i == len(current):
                    replace_0 = current[:i] + ["0"]
                    replace_1 = current[:i] + ["1"]

                else:
                    replace_0 = current[:i] + ["0"] + current[i + 1 :]
                    replace_1 = current[:i] + ["1"] + current[i + 1 :]

                i += 1
                expanded.append((replace_1, i))
                expanded.append((replace_0, i))

                break

        else:
            finished.append(int("".join(current), 2))

    return finished
