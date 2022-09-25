from functools import total_ordering
from copy import deepcopy


@total_ordering
class Cart:
    translation = {">": 0, "^": 1, "<": 2, "v": 3}

    def __init__(self, x: int, y: int, orientation: str, grid: list[list]):
        self.x = x
        self.y = y
        self.orientation = Cart.translation[orientation]
        self.grid = grid
        self.turns = 0

    def move(self):
        if self.orientation == 0:
            self.x += 1
        elif self.orientation == 1:
            self.y -= 1
        elif self.orientation == 2:
            self.x -= 1
        else:
            self.y += 1

        self.change_orientation(self.grid[self.y][self.x])

    def change_orientation(self, tile: str):
        if tile == "|" or tile == "-":
            return
        elif tile == "\\":
            if self.orientation == 0:
                self.orientation = 3
            elif self.orientation == 1:
                self.orientation = 2
            elif self.orientation == 2:
                self.orientation = 1
            else:
                self.orientation = 0
        elif tile == "/":
            if self.orientation == 0:
                self.orientation = 1
            elif self.orientation == 1:
                self.orientation = 0
            elif self.orientation == 2:
                self.orientation = 3
            else:
                self.orientation = 2
        elif tile == "+":
            self.crossroad()

    def crossroad(self):
        if self.turns == 0:
            self.orientation = (self.orientation + 1) % 4
        elif self.turns == 2:
            self.orientation = (self.orientation - 1) % 4
        self.turns = (self.turns + 1) % 3

    def __eq__(self, other):
        return (other.y, other.x) == (self.y, self.x)

    def __lt__(self, other):
        return (other.y, other.x) == (self.y, self.x)

    def __repr__(self):
        return f"Cart({self.x}, {self.y}: {self.orientation})"


def part_1(carts: list) -> tuple:
    while True:
        carts = sorted(carts)
        for i, cart in enumerate(carts):
            cart.move()
            for j, other_cart in enumerate(carts):
                if i == j:
                    continue
                if cart == other_cart:
                    return cart.x, cart.y


def part_2(carts: list) -> tuple:
    while True:
        carts = sorted(carts)
        to_remove = []
        for i, cart in enumerate(carts):
            cart.move()
            for j, other in enumerate(carts):
                if i == j:
                    continue
                if cart == other:
                    to_remove.append(cart)
                    to_remove.append(other)

        for cart in to_remove:
            if cart in carts:
                carts.remove(cart)

        if len(carts) == 1:
            return carts[0].x, carts[0].y


def parse_input():
    with open("input.txt", "r") as file:
        lines = file.readlines()
        carts = []
        grid = [[None for _ in range(len(line))] for line in lines]
        for y, line in enumerate(lines):
            for x, symbol in enumerate(line):
                if symbol in ["|", "-", "\\", "/", "+"]:
                    grid[y][x] = symbol
                else:
                    if symbol in ["^", "v"]:
                        grid[y][x] = "|"
                        carts.append(Cart(x, y, symbol, grid))
                    elif symbol in [">", "<"]:
                        grid[y][x] = "-"
                        carts.append(Cart(x, y, symbol, grid))

        return carts


if __name__ == "__main__":
    cart_list = parse_input()

    print(f"Part 1: The location of the first crash is {part_1(deepcopy(cart_list))}.")

    print(f"Part 2: The final cart ends up at {part_2(cart_list)}.")
