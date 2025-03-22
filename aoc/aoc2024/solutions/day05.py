from functools import cmp_to_key

Rules = set[tuple[int, int]]
Updates = list[list[int]]


def part1(input: str) -> int:
    rules, updates = parse(input)

    correctly_ordered = [
        update for update in updates if is_correctly_ordered(rules, update)
    ]

    return sum([update[len(update) // 2] for update in correctly_ordered])


def part2(input: str) -> int:
    rules, updates = parse(input)

    incorrectly_ordered = filter(
        lambda update: not is_correctly_ordered(rules, update), updates
    )
    fixed_sorting = map(lambda update: sort(rules, update), incorrectly_ordered)

    return sum([update[len(update) // 2] for update in fixed_sorting])


def is_correctly_ordered(rules: Rules, update: list[int]) -> bool:
    return update == sort(rules, update)


def sort(rules: Rules, update: list[int]) -> list[int]:
    def compare(x: int, y: int) -> int:
        return -1 if (x, y) in rules else 1 if (y, x) in rules else 0

    return sorted(update, key=cmp_to_key(compare))


def parse(input: str) -> tuple[Rules, Updates]:
    rule_part, update_part = input.split("\n\n")

    rules = {tuple(map(int, rule.split("|"))) for rule in rule_part.splitlines()}
    updates = [list(map(int, update.split(","))) for update in update_part.splitlines()]

    return (rules, updates)
