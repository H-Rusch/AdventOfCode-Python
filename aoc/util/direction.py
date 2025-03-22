from enum import Enum


class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @staticmethod
    def from_str(input: str) -> "Direction | None":
        match input.lower():
            case "east" | "e" | "right" | "r" | ">":
                return Direction.RIGHT
            case "north" | "n" | "up" | "u" | "^":
                return Direction.UP
            case "west" | "w" | "left" | "l" | "<":
                return Direction.LEFT
            case "south" | "s" | "down" | "d" | "v":
                return Direction.DOWN
            case _:
                return None

    def steps(self, point: tuple[int, int], steps: int = 1) -> tuple[int, int]:
        x, y = point
        match self:
            case Direction.RIGHT:
                return (x + steps, y)
            case Direction.UP:
                return (x, y - steps)
            case Direction.LEFT:
                return (x - steps, y)
            case Direction.DOWN:
                return (x, y + steps)

    def turn_right(self, times: int = 1) -> "Direction":
        return Direction((self.value - times) % len(Direction))

    def turn_left(self, times: int = 1) -> "Direction":
        return Direction((self.value + times) % len(Direction))

    def turn_around(self) -> "Direction":
        return Direction((self.value + 2) % len(Direction))
