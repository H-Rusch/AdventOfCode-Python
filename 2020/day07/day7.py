import re


def part1(rules: list):
    bag_regex = re.compile("(\w* \w*) bag")
    possibilities = 0

    for rule in rules:
        match = bag_regex.findall(rule)
        rule_dict[match[0]] = match[1:]

    searching_for = ["shiny gold"]
    parents = set()

    while searching_for:
        # search parents of an element we are searching for by looking up in which entry's list it is
        searching = searching_for.pop()
        for entry in rule_dict:
            if searching in rule_dict[entry]:
                parents.add(entry)

        # remove the parents from the dictionary
        for entry in parents:
            rule_dict.pop(entry)

        # update the number of possibilities by the number of parent bags
        possibilities += len(parents)

        # add parents to the searching_for list, so their parents can also be found
        searching_for.extend(parents)
        parents.clear()

    print(possibilities)


def part2(rules: list):
    bag_num_regex = re.compile("(no|\d) (\w* \w*) bag")
    # create rule dictionary. The key is the bag outside and for each bag inside an entry in a list is made.
    # That list is the value

    for rule in rules:
        bag_outside = rule[:rule.find("bags") - 1]
        bags = bag_num_regex.findall(rule)
        rule_dict[bag_outside] = bags

    # call recursive method
    print(count_bags("shiny gold"))


def count_bags(bag_name: str):
    # list of bags inside with the information how often they are present
    bags = rule_dict[bag_name]
    # bag has no other bags inside
    if not bags:
        return 0
    # First add how often the bag is present. Then add how many bags are in children bags
    bag_count = 0
    for bag in bags:
        bag_count += int(bag[0])
        bag_count += int(bag[0]) * count_bags(bag[1])
    return bag_count


# read in rules
file = open("input.txt", "r")
rules = file.read().split("\n")
file.close()

rule_dict = dict()
part1(rules)
rule_dict.clear()
part2(rules)
