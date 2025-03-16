import re
from collections import defaultdict


def part1(input: str) -> int:
    template, transformations = parse(input)

    return calculate_after_iterations(template, transformations, 10)


def part2(input: str) -> int:
    template, transformations = parse(input)

    return calculate_after_iterations(template, transformations, 40)


def calculate_after_iterations(template: str, insertion_dict: dict, n: int) -> int:
    # make a dict from the polymer template, mapping how many times each combination appeared
    polymer = defaultdict(int)
    for i in range(len(template) - 1):
        polymer[template[i : i + 2]] += 1

    # make a dict from the letters, mapping how often each letter appeared
    quantity_dict = defaultdict(int)
    for letter in template:
        quantity_dict[letter] += 1

    for _ in range(n):
        pair_counts = defaultdict(int)

        for key in polymer.keys():
            # get the value to insert
            insertion = insertion_dict[key]

            # update how many times each value exists
            quantity_dict[insertion] += polymer[key]

            # update the count how many times each pair exists.
            # The number for the original pair is reset to 0, because a new value was inserted in the pair
            pair_counts[key[0] + insertion] += polymer[key]
            pair_counts[insertion + key[1]] += polymer[key]
            polymer[key] = 0

        polymer = pair_counts

    return max(quantity_dict.values()) - min(quantity_dict.values())


def parse(input: str):
    template, pair_insertions = input.split("\n\n")

    # make a dict for the pair insertions, mapping the pair to the value to be inserted
    transform_dict = dict()
    for transformation in pair_insertions.split("\n"):
        pair, insertion = re.search(r"([A-Z]{2}) -> ([A-Z])", transformation).groups()
        transform_dict[pair] = insertion

    return template, transform_dict
