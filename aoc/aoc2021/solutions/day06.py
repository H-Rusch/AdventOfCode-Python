def part1(input: str) -> int:
    numbers = parse(input)

    return calculate_number_of_fish_in_the_sea(numbers, 80)


def part2(input: str) -> int:
    numbers = parse(input)

    return calculate_number_of_fish_in_the_sea(numbers, 256)


def calculate_number_of_fish_in_the_sea(number_list: list, number_of_days: int) -> int:
    """
    Timer for all fish gets decreased by one each day. If a timer was 0 and it is getting decreased, this fish
    creates offspring. Creating offspring sets the fish's timer to 6 days. The newly created fish starts with a timer
    of 8 days.
    """
    timer_list = [number_list.count(i) for i in range(9)]
    for _ in range(number_of_days):
        fish_created = timer_list[0]
        timer_list = timer_list[1:]
        timer_list[6] += fish_created
        timer_list.append(fish_created)

    return sum(timer_list)


def parse(input: str):
    return [int(s) for s in input.split(",")]
