from enum import Enum
from abc import ABC, abstractmethod

"""
Implementing this task in with the state pattern really lead to much more code than I anticipated.
Source for pattern implementation: https://refactoring.guru/design-patterns/state/python/example
"""


class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    def turn_right(self):
        return Direction((self.value - 1) % len(Direction))

    def turn_left(self):
        return Direction((self.value + 1) % len(Direction))

    def turn_back(self):
        return Direction((self.value + 2) % len(Direction))


class Carrier:
    def __init__(self, position: (int, int)) -> None:
        self.coordinate = position
        self.direction = Direction.UP
        self.infections_caused = 0

    def burst(self, nodes: "NodeDict"):
        current = nodes[self.coordinate]
        self.turn(current)
        self.manipulate_node(current)
        self.move_forward()

    def turn(self, node: "Node"):
        self.direction = node.next_direction(self.direction)

    def manipulate_node(self, node: "Node"):
        node.manipulate()
        if isinstance(node.state, Infected):
            self.infections_caused += 1

    def move_forward(self):
        x, y = self.coordinate
        match self.direction:
            case Direction.RIGHT:
                self.coordinate = (x + 1, y)
            case Direction.UP:
                self.coordinate = (x, y - 1)
            case Direction.LEFT:
                self.coordinate = (x - 1, y)
            case Direction.DOWN:
                self.coordinate = (x, y + 1)


class Infected:
    pass


class Node:
    state = None

    def __init__(self, state: "State") -> None:
        self.transition_to(state)

    def transition_to(self, state: "State"):
        self.state = state
        self.state.context = self

    def next_direction(self, direction: Direction) -> Direction:
        return self.state.next_direction(direction)

    def manipulate(self):
        self.state.transition()


class State(ABC):
    @property
    def context(self) -> Carrier:
        return self._context

    @context.setter
    def context(self, context: Carrier) -> None:
        self._context = context

    @abstractmethod
    def next_direction(self, direction: Direction) -> Direction:
        pass

    @abstractmethod
    def transition(self) -> None:
        pass


class SimpleCleanState(State):
    def next_direction(self, direction: Direction) -> Direction:
        return direction.turn_left()

    def transition(self) -> None:
        self.context.transition_to(SimpleInfectedState())


class SimpleInfectedState(State, Infected):
    def next_direction(self, direction: Direction) -> Direction:
        return direction.turn_right()

    def transition(self) -> None:
        self.context.transition_to(SimpleCleanState())


class CleanState(State):
    def next_direction(self, direction: Direction) -> Direction:
        return direction.turn_left()

    def transition(self) -> None:
        self.context.transition_to(WeakState())


class WeakState(State):
    def next_direction(self, direction: Direction) -> Direction:
        return direction

    def transition(self) -> None:
        self.context.transition_to(InfectedState())


class InfectedState(State, Infected):
    def next_direction(self, direction: Direction) -> Direction:
        return direction.turn_right()

    def transition(self) -> None:
        self.context.transition_to(FlaggedState())


class FlaggedState(State):
    def next_direction(self, direction: Direction) -> Direction:
        return direction.turn_back()

    def transition(self) -> None:
        self.context.transition_to(CleanState())


class NodeDict(dict):
    def __init__(self, simple: bool) -> None:
        self.simple = simple

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            pass

        state = create_clean(self.simple)
        node = Node(state)

        super().__setitem__(key, node)

        return node


def part1(input):
    infected, start_position = parse(input, True)
    carrier = Carrier(start_position)
    perform_bursts(infected, carrier, 10_000)

    return carrier.infections_caused


def part2(input):
    nodes, start_position = parse(input, False)
    carrier = Carrier(start_position)
    perform_bursts(nodes, carrier, 10_000_000)

    return carrier.infections_caused


def perform_bursts(nodes: dict, carrier: Carrier, n: int):
    for _ in range(n):
        carrier.burst(nodes)


def parse(input: str, simple: bool) -> (set[(int, int)], (int, int)):
    nodes = NodeDict(simple)
    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                state = create_infected(simple)
                nodes[(x, y)] = Node(state)

    start_position = (
        len(input.splitlines()[0]) // 2, len(input.splitlines()) // 2)

    return nodes, start_position


def create_infected(simple: bool):
    return SimpleInfectedState() if simple else InfectedState()


def create_clean(simple: bool):
    return SimpleCleanState() if simple else CleanState()
