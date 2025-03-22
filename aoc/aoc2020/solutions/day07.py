import re


BAG_NUMBER_PATTERN = re.compile(r"(no|\d) (\w* \w*) bag")


def part1(input):
    bag_contents = parse(input)

    return count_possibilities(bag_contents, "shiny gold")


def part2(input):
    rule_dict = parse(input)

    # count recursively
    return count_bags("shiny gold", rule_dict)


def count_possibilities(bag_contents: dict, initial_search: str) -> int:
    possibilities = 0
    parents = set()
    searching = [initial_search]

    while len(searching) > 0:
        # search parents of an element we are searching for by looking up in which entry's list it is
        current = searching.pop()

        for bag, bag_content in bag_contents.items():
            contained_bags = {bag for (_, bag) in bag_content}
            if current in contained_bags:
                parents.add(bag)

        # remove the parents from the dictionary
        for bag in parents:
            bag_contents.pop(bag)

        # update the number of possibilities by the number of parent bags
        possibilities += len(parents)

        # expand search to the parents of the current bag
        searching.extend(parents)
        parents.clear()

    return possibilities


def count_bags(bag_name: str, rule_dict: dict):
    contained_bags = rule_dict[bag_name]

    if len(contained_bags) == 0:
        return 0

    # First add how often the bag is present. Then add how many bags are in children bags
    bag_count = 0
    for n, bag_name in contained_bags:
        bag_count += n
        bag_count += n * count_bags(bag_name, rule_dict)

    return bag_count


def parse(input: str) -> dict[str, list[(int, str)]]:
    bag_contents = {}

    for rule in input.splitlines():
        bag = rule[: rule.find("bags") - 1]
        contained_bags = [
            (int(n), description) for n, description in BAG_NUMBER_PATTERN.findall(rule)
        ]
        bag_contents[bag] = contained_bags

    return bag_contents
