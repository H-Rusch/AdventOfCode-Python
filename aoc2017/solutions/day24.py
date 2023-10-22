import math
from collections.abc import Iterator


class BridgeGenerator:
    def __init__(self, components: list[(int, int)]) -> None:
        self.components = set(components)
        self.max_strength = -math.inf
        self.longest_length = 0
        self.longest = []

    def generate(self):
        self.generate_helper([], set(), 0)

    def generate_helper(self, bridge: list, visited: set, open_port: int):
        for component in self.possible_pieces(open_port, visited):
            next_port = self.next_open_port(open_port, *component)
            next_brigde = bridge[:] + [component]
            visited.add(component)
            self.generate_helper(next_brigde, visited, next_port)
            visited.remove(component)

        self.adjust_max_strength(bridge)
        self.adjust_longest(bridge)

    def possible_pieces(self, open_port: int, visited: set) -> Iterator[(int, int)]:
        for (port1, port2) in self.components - visited:
            if port1 == open_port or port2 == open_port:
                yield (port1, port2)

    def next_open_port(self, open_port: int, port1: int, port2: int) -> int:
        if port1 == port2:
            return port1
        if open_port == port1:
            return port2
        if open_port == port2:
            return port1

    def adjust_max_strength(self, bridge: list[(int, int)]):
        bridge_strength = BridgeGenerator.bridge_strength(bridge)
        self.max_strength = max(self.max_strength, bridge_strength)

    @classmethod
    def bridge_strength(cls, bridge: list[(int, int)]) -> int:
        return sum(port1 + port2 for (port1, port2) in bridge)

    def adjust_longest(self, bridge: list):
        if len(bridge) > self.longest_length:
            self.longest_length = len(bridge)
            self.longest = []
        if len(bridge) == self.longest_length:
            self.longest.append(bridge)


def part1(input):
    components = parse(input)

    generator = BridgeGenerator(components)
    generator.generate()

    return generator.max_strength


def part2(input):
    components = parse(input)

    generator = BridgeGenerator(components)
    generator.generate()

    return max(map(BridgeGenerator.bridge_strength, generator.longest))


def parse(input: str) -> list[(int, int)]:
    return [tuple(map(int, line.split("/"))) for line in input.splitlines()]
