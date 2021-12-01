def part_1(number_list):
    times_increasing = 0

    for i in range(1, len(number_list)):
        if number_list[i - 1] < number_list[i]:
            times_increasing += 1

    print(f"Part 1: The numbers increase {times_increasing} times.")


def part_2(number_list):
    times_increasing = 0

    for i in range(3, len(number_list)):
        if sum(number_list[i - 4:i - 1]) < sum(number_list[i - 3:i]):
            times_increasing += 1

    print(f"Part 2: The value of the sums increases {times_increasing} times.")


if __name__ == "__main__":
    with open("input.txt", 'r', encoding='utf-8') as file:
        numbers = [int(s) for s in file.read().splitlines()]

        part_1(numbers)

        part_2(numbers)
