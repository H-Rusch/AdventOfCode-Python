from functools import reduce

class Packet:
    def __init__(self, version: str, type_id: int):
        self.version = version
        self.type_id = type_id


class OperatorPacket(Packet):
    def __init__(self, version: str, type_id: int, children: list):
        super().__init__(version, type_id)

        self.children = children
        
    def calculate(self) -> int:
        if self.type_id == 0:
            return reduce(lambda x, y: x + y, map(lambda p: p.calculate(), self.children))
        elif self.type_id == 1:
            return reduce(lambda x, y: x * y, map(lambda p: p.calculate(), self.children))
        elif self.type_id == 2:
            return min(map(lambda p: p.calculate(), self.children))
        elif self.type_id == 3:
            return max(map(lambda p: p.calculate(), self.children))
        elif self.type_id == 5:
            return 1 if self.children[0].calculate() > self.children[1].calculate() else 0
        elif self.type_id == 6:
            return 1 if self.children[0].calculate() < self.children[1].calculate() else 0
        else:
            return 1 if self.children[0].calculate() == self.children[1].calculate() else 0


class ValuePacket(Packet):
    def __init__(self, version: str, type_id: int, value: int):
        super().__init__(version, type_id)

        self.value = value
        
    def calculate(self) -> int:
        return self.value


def part_1(packet: Packet) -> int:
    total = summed_versions(packet)

    return total


def part_2(packet: OperatorPacket) -> int:
    return packet.calculate()


def summed_versions(packet: Packet) -> int:
    if isinstance(packet, ValuePacket):
        return int(packet.version, 2)

    if isinstance(packet, OperatorPacket):
        return int(packet.version, 2) + sum(map(lambda c: summed_versions(c), packet.children))


def parse_packet(binary_representation: str, i: int) -> tuple:
    version = binary_representation[i: i + 3]
    i += 3
    type_id = int(binary_representation[i: i + 3], 2)
    i += 3

    # literal value
    if type_id == 4:
        i, node = create_literal_packet(binary_representation, i, version, type_id)

    # operator node
    else:
        i, node = create_operator_packet(binary_representation, i, version, type_id)

    return i, node


def create_operator_packet(bin_representation: str, i: int, version: str, type_id: int) -> tuple:
    length_type = bin_representation[i]
    i += 1

    children = []

    if length_type == "0":
        total_length = int(bin_representation[i: i + 15], 2)
        i += 15

        subpacket_size = 0
        tmp_i = i
        while subpacket_size != total_length:
            i, child_packet = parse_packet(bin_representation, i)
            children.append(child_packet)

            subpacket_size += i - tmp_i
            tmp_i = i

    else:
        num_sub = int(bin_representation[i:i + 11], 2)
        i += 11

        for _ in range(num_sub):
            i, child_packet = parse_packet(bin_representation, i)
            children.append(child_packet)

    packet_created = OperatorPacket(version, type_id, children)

    return i, packet_created


def create_literal_packet(bin_representation: str, i: int, version: str, type_id: int) -> tuple:
    value = ""
    size = 0
    while True:
        part = bin_representation[i + size: i + size + 5]
        value += part[1:]

        size += 5

        if part[0] == "0":
            break

    return i + size, ValuePacket(version, type_id, int(value, 2))


def convert_to_full_binary(hex_representation: str) -> str:
    return "".join([bin(int(h, 16))[2:].zfill(4) for h in hex_representation])


def parse_input():
    with open("input.txt", "r") as file:
        return file.read().strip()


if __name__ == "__main__":
    hex_string = parse_input()

    binary = convert_to_full_binary(hex_string)
    _, packet = parse_packet(binary, 0)

    print(f"Part 1: The sum of all version numbers is {part_1(packet)}.")

    print(f"Part 2: Calculating the function the packet describes gives the value {part_2(packet)}.")
