def part_1(number_list: list) -> int:
    times_increasing = 0

    for i in range(1, len(number_list)):
        if number_list[i - 1] < number_list[i]:
            times_increasing += 1

    return times_increasing


def part_2(number_list: list) -> int:
    times_increasing = 0

    for i in range(3, len(number_list)):
        if sum(number_list[i - 4:i - 1]) < sum(number_list[i - 3:i]):
            times_increasing += 1

    return times_increasing


def parse_input():
    with open("input.txt", 'r', encoding='utf-8') as file:
        return [int(s) for s in file.read().splitlines()]


if __name__ == "__main__":
    numbers = parse_input()

    print(f"Part 1: The numbers increase {part_1(numbers)} times.")

    print(f"Part 2: The value of the sums increases {part_2(numbers)} times.")
