def part_1(number_list: list) -> int:
    return calculate_number_of_fish_in_the_sea(number_list, 80)


def part_2(number_list: list) -> int:
    return calculate_number_of_fish_in_the_sea(number_list, 256)


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


def parse_input():
    with open("input.txt", "r") as file:
        return [int(s) for s in file.read().split(",")]


if __name__ == "__main__":
    numbers = parse_input()

    print(f"Part 1: After 80 days there are a total of {part_1(numbers)} fish.")

    print(f"Part 2: After 256 days there are a total of {part_2(numbers)} fish.")
