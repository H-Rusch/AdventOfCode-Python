import functools


def part1(input):
    ingredient_list = parse(input)

    _, counter = build_allergen_dict(ingredient_list)

    return counter


def part2(input):
    ingredient_list = parse(input)

    allergen_dict, _ = build_allergen_dict(ingredient_list)

    return ",".join(allergen_dict[ing][0] for ing in sorted(allergen_dict))


def build_allergen_dict(ingredient_list):
    important_ingredients = list()
    # create a dictionary which maps in which ingredients the different allergens are
    allergen_dict = dict()
    for entry in ingredient_list:
        allergens = entry[entry.find("(contains ") + 10 : entry.find(")")]
        ingredients = entry[: entry.find("(") - 1].split(" ")
        important_ingredients.extend(ingredients)

        for allergen in allergens.split(", "):
            if allergen in allergen_dict.keys():
                allergen_dict[allergen].append(ingredients)
            else:
                allergen_dict[allergen] = [ingredients]

    # intersect the sub-lists of ingredients, because if an allergen is in 2 recipes, it has to be in the shared ingred.
    for entry in allergen_dict.items():
        allergen_dict[entry[0]] = list(
            functools.reduce(lambda a, b: set(a).intersection(b), entry[1])
        )

    # if the matching allergen for an ingredient is found, it is removed from the possibilities of all other ingredients
    # if a change is made, another repetition is made
    repeat = True
    while repeat:
        repeat = False
        for entry in allergen_dict.items():
            if len(allergen_dict[entry[0]]) == 1:
                for other_entry in allergen_dict.items():
                    if other_entry[0] != entry[0] and entry[1][0] in other_entry[1]:
                        other_entry[1].remove(entry[1][0])
                        repeat = True

    # find the ingredients which have no allergen in them and count how often those appear in the ingredient list
    allergen_ingredients = []
    for ing in allergen_dict.values():
        allergen_ingredients += ing
    important_ingredients = [
        ing for ing in set(important_ingredients) if ing not in allergen_ingredients
    ]

    counter = 0
    for entry in ingredient_list:
        for ing in entry[: entry.find("(") - 1].split(" "):
            if ing in important_ingredients:
                counter += 1

    return allergen_dict, counter


def parse(input):
    return [ingredients for ingredients in input.splitlines()]
