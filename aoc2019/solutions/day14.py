import math
from collections import defaultdict

TRILLION = 1_000_000_000_000


def part1(input) -> int:
    rules = parse(input)

    return calculate_ore_for_fuel(rules, 1)


def part2(input) -> int:
    rules = parse(input)

    cost_for_one = calculate_ore_for_fuel(rules, 1)
    n = int(TRILLION / cost_for_one)

    left, right = n, TRILLION
    middle = 12
    while left + 1 < right:
        middle = int((right + left) / 2)
        ore_amount = calculate_ore_for_fuel(rules, middle)

        if ore_amount < TRILLION:
            left = middle
        elif ore_amount > TRILLION:
            right = middle
        else:
            break

    return middle


def calculate_ore_for_fuel(rules: dict, amount_of_fuel: int) -> int:
    ore_count = 0
    needed = [{"item": "FUEL", "amount": amount_of_fuel}]
    supply = defaultdict(int)

    while len(needed) > 0:
        element = needed.pop(0)
        chemical, required_amount = element["item"], element["amount"]

        if chemical == "ORE":
            # count ores which have to be mined
            ore_count += required_amount

        else:
            if chemical in supply:
                # use ingredients stored in the supply
                if required_amount <= supply[chemical]:
                    supply[chemical] -= required_amount
                    required_amount = 0
                else:
                    required_amount -= supply[chemical]
                    supply[chemical] = 0

            creating_amount, ingredients = (
                rules[chemical]["created"],
                rules[chemical]["ingredients"],
            )

            mult = math.ceil(required_amount / creating_amount)
            if mult * creating_amount > required_amount:
                supply[chemical] += mult * creating_amount - required_amount

            needed.extend(
                list(
                    map(
                        lambda i: {"amount": mult * i["amount"], "item": i["item"]},
                        ingredients,
                    )
                )
            )

    return ore_count


def parse(input):
    def make_ingredient(ingredient: str) -> dict:
        a, i = ingredient.split()
        return {"amount": int(a), "item": i}

    rules = dict()
    for line in input.splitlines():
        consumes, produces = line.split(" => ")

        inputs = [make_ingredient(c) for c in consumes.split(", ")]
        output = make_ingredient(produces)

        rules[output["item"]] = {"created": output["amount"], "ingredients": inputs}
    return rules


if __name__ == "__main__":
    rule_dict = parse(input)

    print(
        f"Part 1: The minimum amount of ore needed to produce one unit of fuel is {part1(rule_dict)}."
    )

    print(
        f"Part 2: With 1 trillion ore, {part2(rule_dict)} units of fuel can be created."
    )
