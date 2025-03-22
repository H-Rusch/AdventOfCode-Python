class Recipe:
    def __init__(self):
        self.state = [3, 7]
        self.i1, self.i2 = 0, 1

    def make_new_recipe(self):
        elf1 = self.state[self.i1]
        elf2 = self.state[self.i2]

        combined = elf1 + elf2
        if combined >= 10:
            self.state.append(combined // 10)
        self.state.append(combined % 10)

        self.i1 = (self.i1 + 1 + elf1) % len(self.state)
        self.i2 = (self.i2 + 1 + elf2) % len(self.state)


def part1(input: str) -> str:
    limit = int(input)
    recipe = Recipe()

    while len(recipe.state) < limit + 10:
        recipe.make_new_recipe()

    return "".join([str(r) for r in recipe.state[-10:]])


def part2(searching: str) -> int:
    recipe = Recipe()

    while True:
        if len(recipe.state) > len(searching):
            if (
                "".join([str(r) for r in recipe.state[-len(searching) - 1 : -1]])
                == searching
            ):
                return len(recipe.state) - len(searching) - 1
            if "".join([str(r) for r in recipe.state[-len(searching) :]]) == searching:
                return len(recipe.state) - len(searching)

        recipe.make_new_recipe()
