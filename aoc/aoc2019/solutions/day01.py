def part1(input) -> int:
    mass_list = parse(input)

    return sum([get_fuel_for_mass(mass) for mass in mass_list])


def part2(input) -> int:
    mass_list = parse(input)

    return sum([get_all_fuel_for_mass(mass) for mass in mass_list])


def get_all_fuel_for_mass(mass: int) -> int:
    if mass <= 0:
        return 0

    fuel = get_fuel_for_mass(mass)
    return get_all_fuel_for_mass(fuel) + fuel


def get_fuel_for_mass(mass: int) -> int:
    return max(int(mass / 3) - 2, 0)


def parse(input):
    return [int(s) for s in input.splitlines()]
