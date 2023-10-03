def part1(mass_list: list) -> int:
    return sum([get_fuel_for_mass(mass) for mass in mass_list])


def part2(mass_list: list) -> int:
    return sum([get_all_fuel_for_mass(mass) for mass in mass_list])


def get_all_fuel_for_mass(mass: int) -> int:
    if mass <= 0:
        return 0

    fuel = get_fuel_for_mass(mass)
    return get_all_fuel_for_mass(fuel) + fuel


def get_fuel_for_mass(mass: int) -> int:
    return max(int(mass / 3) - 2, 0)


def parse(input):
    with open("input.txt", "r") as file:
        return [int(s) for s in file.read().splitlines()]


if __name__ == "__main__":
    number_list = parse(input)

    print(f"Part 1: The sum of fuel requirements for all modules is {part1(number_list)}.")

    print(f"Part 2: The sum of fuel requirements with the additional fuel for all modules is {part2(number_list)}.")
